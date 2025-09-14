## Django Security Settings
- **SECURE_SSL_REDIRECT = True** → Forces all traffic to HTTPS.
- **SECURE_HSTS_SECONDS = 31536000** → Enforces HTTPS in browsers for 1 year.
- **SECURE_HSTS_INCLUDE_SUBDOMAINS = True** → Applies HSTS to all subdomains.
- **SECURE_HSTS_PRELOAD = True** → Allows site to be included in browser preload lists.
- **SESSION_COOKIE_SECURE = True** → Session cookies only sent over HTTPS.
- **CSRF_COOKIE_SECURE = True** → CSRF cookies only sent over HTTPS.
- **X_FRAME_OPTIONS = 'DENY'** → Protects against clickjacking.
- **SECURE_CONTENT_TYPE_NOSNIFF = True** → Prevents MIME-type sniffing.
- **SECURE_BROWSER_XSS_FILTER = True** → Enables basic XSS filtering.

## Web Server (Example: Nginx)
To fully support HTTPS in production, configure SSL/TLS certificates:

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        include proxy_params;
    }
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}

