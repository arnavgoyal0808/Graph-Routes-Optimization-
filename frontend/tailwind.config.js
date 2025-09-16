/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'logichain-blue': '#667eea',
        'logichain-purple': '#764ba2',
      }
    },
  },
  plugins: [],
}
