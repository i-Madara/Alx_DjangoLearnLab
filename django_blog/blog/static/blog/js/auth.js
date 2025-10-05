console.log('auth.js loaded on login/register');

document.addEventListener('DOMContentLoaded', () => {
  const firstInput = document.querySelector('form input[type="text"], form input[type="email"], form input[type="password"]');
  if (firstInput) firstInput.focus();
});
