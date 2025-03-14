FROM postgres:14-alpine

# Health check script
COPY docker/postgres/healthcheck.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/healthcheck.sh

HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 CMD ["healthcheck.sh"]