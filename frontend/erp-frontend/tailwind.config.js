/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2F4F4F', // Obsidian Green 216
        accent: '#B8860B',  // DarkGoldenRod for luxury accent
        'light-neutral': '#F8F8F8', // WhiteSmoke for light backgrounds
        'dark-neutral': '#36454F',  // Charcoal for dark text/elements
        danger: '#EF4444', // Keep existing danger color
      }
    },
  },
  plugins: [],
}
