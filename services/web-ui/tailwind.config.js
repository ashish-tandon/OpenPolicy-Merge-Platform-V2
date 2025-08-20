/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'op-blue': '#1A59C7',
        'op-gray': '#DDDDDD',
        'op-dark': '#333333',
      },
      maxWidth: {
        'text': '40rem',
      }
    },
  },
  plugins: [],
}
