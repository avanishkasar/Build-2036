/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./public/index.html"],
  theme: {
    extend: {
      colors: {
        paper: "#F4EEE3",
        card: "#FAF6EE",
        ink: "#1E1B18",
        muted: "#6B6358",
        line: "#DDD3C3",
        forest: { DEFAULT: "#1F4D3A", deep: "#163A2C" },
        allow: { DEFAULT: "#1F5E3F", soft: "#DCE8DC" },
        pin: { DEFAULT: "#8A5A12", soft: "#F2E2C4" },
        block: { DEFAULT: "#9A3B2F", soft: "#F1DFDA" },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        serif: ["Instrument Serif", "Georgia", "serif"],
      },
    },
  },
  plugins: [],
};
