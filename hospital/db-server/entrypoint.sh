#!/bin/bash
set -e

# If weak credentials vulnerability is enabled, override the database password
# with a trivially guessable one before PostgreSQL initializes
if [ "${VULN_WEAK_CREDS}" = "true" ]; then
    export POSTGRES_PASSWORD="hospital123"
fi

# If excessive privileges vulnerability is enabled, append a SQL statement
# that grants the hospital user superuser rights after initialization
if [ "${VULN_EXCESSIVE_PRIVS}" = "true" ]; then
    cat >> /docker-entrypoint-initdb.d/init.sql << 'EOF'

-- VULN: hospitaluser granted superuser privileges
ALTER USER hospitaluser WITH SUPERUSER;
EOF
fi

# Hand off to the official PostgreSQL entrypoint
exec docker-entrypoint.sh postgres