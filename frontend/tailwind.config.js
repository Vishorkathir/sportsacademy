/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#ff6b35',
        secondary: '#004e89',
        accent: '#f7931e',
        dark: '#0f1419',
        light: '#f5f5f5',
      },
      animation: {
        'bounce-slow': 'bounce 2s infinite',
        'float': 'float 15s infinite ease-in-out',
        'slide-in': 'slideIn 0.8s ease-out',
        'fade-in': 'fadeIn 0.8s ease-out',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translate(0, 0)' },
          '25%': { transform: 'translate(20px, -20px)' },
          '50%': { transform: 'translate(0, 40px)' },
          '75%': { transform: 'translate(-20px, -10px)' },
        },
        slideIn: {
          '0%': { opacity: '0', transform: 'translateX(-50px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
