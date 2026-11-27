"""Build the ADHIKAR demo video: narration, timed screen recording, burned captions.

Usage:
  python video/build.py --url http://localhost:8765 --out out/

Narration uses Google Cloud Text-to-Speech Chirp 3 HD voices. The API key is injected
by the environment's network proxy (header X-Goog-Api-Key), so no key is read here.
Without narration the script still renders a captioned video timed at 147 words a minute.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
VOICES = ["en-IN-Chirp3-HD-Kore", "en-IN-Chirp3-HD-Aoede", "en-US-Chirp3-HD-Kore", "en-IN-Neural2-A"]
TTS_URL = "https://texttospeech.googleapis.com/v1/text:synthesize"
GAP = 0.45  # seconds of breath between segments
WPM = 147


def tts(text: str, out: Path) -> str | None:
    for voice in VOICES:
        body = json.dumps({
            "input": {"text": text},
            "voice": {"languageCode": voice[:5], "name": voice},
            "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 48000, "speakingRate": 1.0},
        }).encode()
        req = urllib.request.Request(TTS_URL, data=body, headers={"content-type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                out.write_bytes(base64.b64decode(json.load(r)["audioContent"]))
                return voice
        except urllib.error.HTTPError as e:
            print(f"  {voice}: HTTP {e.code} {e.read()[:200]!r}", file=sys.stderr)
        except urllib.error.URLError as e:
            print(f"  {voice}: {e.reason}", file=sys.stderr)
            return None
    return None


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def srt_time(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def chunks(text: str, max_chars: int = 84) -> list[str]:
    """Split into caption chunks at sentence and clause breaks, at most two short lines each."""
    parts = re.split(r"(?<=[.!?,])\s+", text)
    out: list[str] = []
    cur = ""
    for p in parts:
        if cur and len(cur) + 1 + len(p) > max_chars:
            out.append(cur)
            cur = p
        else:
            cur = f"{cur} {p}".strip()
        while len(cur) > max_chars:
            cut = cur.rfind(" ", 0, max_chars)
            out.append(cur[:cut])
            cur = cur[cut + 1:]
    if cur:
        out.append(cur)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://localhost:8765")
    ap.add_argument("--out", default=str(HERE / "out"))
    ap.add_argument("--no-tts", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    segs = json.loads((HERE / "script.json").read_text())

    voiced = not a.no_tts
    voice_used = None
    for s in segs:
        wav = out / f"{s['id']}.wav"
        if voiced and not wav.exists():
            print(f"TTS {s['id']}")
            voice_used = tts(s["text"], wav)
            if voice_used is None:
                print("Narration unavailable, rendering captions only", file=sys.stderr)
                voiced = False
        s["dur"] = duration(wav) if voiced else len(s["text"].split()) / WPM * 60
        s["dur"] += GAP

    # Captions
    t = 0.0
    lines: list[str] = []
    n = 1
    for s in segs:
        cs = chunks(s["text"])
        total = sum(len(c) for c in cs)
        ct = t
        for c in cs:
            d = (s["dur"] - GAP) * len(c) / total
            lines += [str(n), f"{srt_time(ct)} --> {srt_time(ct + d)}", c, ""]
            ct += d
            n += 1
        s["start"] = t
        t += s["dur"]
    (out / "captions.srt").write_text("\n".join(lines))
    (out / "timeline.json").write_text(json.dumps([{"id": s["id"], "action": s["action"], "dur": s["dur"]} for s in segs]))
    print(f"Total {t:.1f}s, voiced={voiced} voice={voice_used}")

    # Screen recording
    subprocess.run(["node", str(HERE / "record.js"), a.url, str(out)], check=True)
    raw = next(out.glob("raw/*.webm"))

    # Audio track
    audio_args: list[str] = []
    if voiced:
        concat = out / "audio.txt"
        silence = out / "gap.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", str(GAP), str(silence)], check=True)
        concat.write_text("".join(f"file '{out / (s['id'] + '.wav')}'\nfile '{silence}'\n" for s in segs))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-ar", "48000", str(out / "narration.wav")], check=True)
        audio_args = ["-i", str(out / "narration.wav"), "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k"]

    style = "FontName=Inter,FontSize=15,PrimaryColour=&H00FFFFFF,BackColour=&H99161E1A,BorderStyle=4,Outline=0,Shadow=0,MarginV=34,Alignment=2"
    vf = f"scale=1920:1080:flags=lanczos,subtitles={out / 'captions.srt'}:fontsdir={HERE.parent / 'public' / 'fonts'}:force_style='{style}'"
    final = out / ("ADHIKAR_demo.mp4" if voiced else "ADHIKAR_demo_captions_only.mp4")
    lead = (out / "lead.txt").read_text().strip()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", lead, "-i", str(raw), *audio_args, "-vf", vf,
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30",
                    "-t", f"{t:.2f}", "-movflags", "+faststart", str(final)], check=True)
    print(f"Wrote {final} ({duration(final):.1f}s)")


if __name__ == "__main__":
    main()
