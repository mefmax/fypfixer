/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          teal: '#208E9F',
          orange: '#FF6B35',
          purple: '#A855F7',
        },
        dark: {
          bg: '#0F172A',
          secondary: '#1A1F3A',
        }
      },
    },
  },
  plugins: [],
}
