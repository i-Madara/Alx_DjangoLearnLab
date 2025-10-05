console.log('auth.js loaded on login/register');
document.addEventListener('DOMContentLoaded', () => {
  const first = document.querySelector('form input[type="text"], form input[type="email"], form input[type="password"]');
  if (first) first.focus();
});
