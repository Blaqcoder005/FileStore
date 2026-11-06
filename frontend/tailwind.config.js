/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: "#4256A3", hover: "#5278C5" },
        dark: "#4A397B",
        accent: "#A07DC7",
        tint: "#D2ABEF",
        surface: "#F7F5FB",
        ink: "#1E1B2E",
        teal: {
          50:  "#E4EDEC", // lightest — page backgrounds, subtle surfaces
          100: "#ADC3C9", // muted borders, dividers, disabled states
          300: "#5C7687", // secondary text, icons, placeholders
          500: "#039AA1", // primary accent / brand (buttons, links)
          600: "#096472", // hover / active state of primary
          800: "#13404E", // dark surfaces, headers, cards on dark bg
          900: "#042023", // near-black backgrounds, deepest surfaces
        },
      },
    },
  },
  plugins: [],
};
