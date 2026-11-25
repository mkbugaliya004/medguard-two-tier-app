
FROM nginx:alpine

# Copy frontend HTML
COPY index.html /usr/share/nginx/html/index.html

# Copy CSS and JavaScript
COPY css/ /usr/share/nginx/html/css/
COPY login.html /usr/share/nginx/html/login.html
COPY js/ /usr/share/nginx/html/js/

# Copy custom MedGuard icons
COPY assets/ /usr/share/nginx/html/assets/

# Copy PWA manifest
COPY manifest.json /usr/share/nginx/html/manifest.json

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
