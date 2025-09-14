# Security Measures

- **DEBUG = False** for production.
- Enabled `SECURE_BROWSER_XSS_FILTER`, `SECURE_CONTENT_TYPE_NOSNIFF`, and `X_FRAME_OPTIONS`.
- Enforced HTTPS-only cookies with `CSRF_COOKIE_SECURE` and `SESSION_COOKIE_SECURE`.
- All forms include `{% csrf_token %}` to prevent CSRF attacks.
- Views use Django ORM and `forms.Form` validation to prevent SQL injection.
- Added Content Security Policy (CSP) setup via `django-csp` middleware.
