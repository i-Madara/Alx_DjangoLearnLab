console.log('base app.js loaded');

document.addEventListener('DOMContentLoaded', () => {
  const forms = document.querySelectorAll('form[novalidate]');
  forms.forEach(f => {
    f.addEventListener('submit', () => {
      console.log('Submitting form:', f.action || window.location.pathname);
    });
  });
});
