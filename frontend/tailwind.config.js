/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'st-blue-dark': '#1e5481',
        'st-blue': '#5899c4',
        'st-blue-light': '#a8d5f2',
        'st-green': '#8cc63f',
        'st-green-dark': '#6fa32e',
        'st-orange': '#f26430',
        'st-navy': '#2c3e50',
      },
      fontFamily: {
        sans: ['system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
