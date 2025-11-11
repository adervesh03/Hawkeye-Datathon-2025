# frontend/Dockerfile
FROM nginx:alpine

# Cloud Run expects the app to listen on $PORT.
# NGINX default is 80/8080; we’ll set it via a custom conf.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the static build output
COPY dist /usr/share/nginx/html