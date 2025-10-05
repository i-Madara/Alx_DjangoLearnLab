console.log('base app.js loaded');
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('form[novalidate]').forEach(f => {
    f.addEventListener('submit', () => console.log('Submitting:', f.action || location.pathname));
  });
});
