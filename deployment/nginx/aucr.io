server {
# listen on port 80 (http)
listen 80;
server_name _;
location / {
# redirect any requests to the same URL but on https
return 301 https://$host$request_uri;
}
}
server {
# listen on port 443 (https)
listen 443 ssl;
server_name _;
# location of the self-signed SSL certificate
ssl_certificate /etc/nginx/ssl/fullchain.pem;
ssl_certificate_key /etc/nginx/ssl/privkey.pem;
# write access and error logs to /var/log
access_log /var/log/aucr_access.log;
error_log /var/log/aucr_error.log;
location / {
# forward application requests to the gunicorn server
proxy_pass http://10.100.0.206:5000;
proxy_redirect off;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
location /static {
# handle static files directly, without forwarding to the application
alias /opt/aucr/aucr_app/plugins/main/static;
expires 30d;
}
location /socket.io {
    proxy_pass http://10.100.0.206:5000/socket.io;
}
}
