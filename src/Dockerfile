FROM tiangolo/uwsgi-nginx:python3.7

# Expose the web-server local port
ENV LISTEN_PORT 8080
EXPOSE 8080

# Define environment
COPY ./app /app
RUN echo ${groupid} > /app/models/.env
WORKDIR /app
ENV PYTHONPATH=/app

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Move the base entrypoint to reuse it
RUN mv /entrypoint.sh /uwsgi-nginx-entrypoint.sh
# Copy the entrypoint that will generate Nginx additional configs
COPY entrypoint.sh /entrypoint.sh

# Run the entrypoint configuration
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Allow waiting script to be executed
RUN chmod +x ./wait-for-it.sh

# Hold the webserver from launching until the database is ready with 50s timeout
CMD ["./wait-for-it.sh", "-t", "50", "-h", "10.${groupid}.0.5", "db:3306", "--", "/start.sh"]
