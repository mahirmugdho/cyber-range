#!/bin/bash
set -e

# If weak SSH credentials vulnerability is enabled, set a trivially
# guessable password on the nurse_user account
if [ "${VULN_WEAK_SSH}" = "true" ]; then
    echo "nurse_user:nurse123" | chpasswd
fi

# If sensitive files vulnerability is enabled, make the db_notes file
# world-readable and drop an additional plaintext credentials file
if [ "${VULN_SENSITIVE_FILES}" = "true" ]; then
    chmod 644 /home/nurse_user/documents/db_notes.txt
    echo "hospitaluser:hospital123" > /home/nurse_user/documents/db_creds.txt
    chmod 644 /home/nurse_user/documents/db_creds.txt
fi

# If SUID vulnerability is enabled, set the SUID bit on a binary
# that can be exploited for privilege escalation
if [ "${VULN_SUID}" = "true" ]; then
    chmod u+s /usr/bin/find
fi

# Start the SSH daemon in the foreground
exec /usr/sbin/sshd -D