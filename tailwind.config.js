/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: ["./templates/**/*.{html,htm}"],
  theme: {
    extend: {
      colors: {
        first: "#E7E8E7",
        second: "#87BFDA",
        third: "#87BFDA",
        forth: "#2C6485",
      }
    },
  },
  plugins: [],
}

