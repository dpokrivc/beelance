#! /usr/bin/env bash
set -e

/uwsgi-nginx-entrypoint.sh

# Get the URL for static files from the environment variable
USE_STATIC_URL=${STATIC_URL:-'/static'}
# Get the absolute path of the static files from the environment variable
USE_STATIC_PATH=${STATIC_PATH:-'/app/static'}
# Get the listen port for Nginx, default to 8080
USE_LISTEN_PORT=${LISTEN_PORT:-8080}

#if [ -f /app/nginx.conf ]; then
#    cat /app/nginx.conf > /etc/nginx/conf.d/nginx.conf
#else
content_server='server {\n'
content_server=$content_server"    listen ${USE_LISTEN_PORT};\n"
content_server=$content_server'    location / {\n'
content_server=$content_server'        include uwsgi_params;\n'
content_server=$content_server'        uwsgi_pass unix:///tmp/uwsgi.sock;\n'
content_server=$content_server'    }\n'
content_server=$content_server"    location $USE_STATIC_URL {\n"
content_server=$content_server"        alias $USE_STATIC_PATH;\n"
content_server=$content_server'    }\n'
content_server=$content_server'}\n'


# Configuration skeleton for using SSL
# https://nginx.org/en/docs/http/configuring_https_servers.html
#content_server=$content_server'server {\n'
#content_server=$content_server"    listen 443 ssl http2;\n"
#content_server=$content_server'    ssl_certificate      <certificate .crt file>;\n'
#content_server=$content_server'    ssl_certificate_key     <certificate .key file>;\n'
#content_server=$content_server'    ssl_protocols       <optional protocols>;\n'
#content_server=$content_server'    ssl_ciphers         <optional ciphers>;\n'
#content_server=$content_server'    location / {\n'
#content_server=$content_server'        include uwsgi_params;\n'
#content_server=$content_server'        uwsgi_pass unix:///tmp/uwsgi.sock;\n'
#content_server=$content_server'    }\n'
#content_server=$content_server"    location $USE_STATIC_URL {\n"
#content_server=$content_server"        alias $USE_STATIC_PATH;\n"
#content_server=$content_server'    }\n'
#content_server=$content_server'}\n'


# Save generated server /etc/nginx/conf.d/nginx.conf
printf "$content_server" > /etc/nginx/conf.d/nginx.conf

exec "$@"