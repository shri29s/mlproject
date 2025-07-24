/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../templates/**/*.html", // ✅ Flask Jinja2 templates
    "../templates/*.html", // ✅ Flask Jinja2 templates (backup)
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
