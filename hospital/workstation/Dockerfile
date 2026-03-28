FROM ubuntu:24.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install core packages
RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    curl \
    wget \
    net-tools \
    iputils-ping \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create a low-privilege user simulating a nurse workstation account
RUN useradd -m -s /bin/bash nurse_user && \
    echo "nurse_user:nursepass123" | chpasswd

# Create a higher-privilege admin user
RUN useradd -m -s /bin/bash ws_admin && \
    echo "ws_admin:$(openssl rand -base64 16)" | chpasswd

# Set up SSH
RUN mkdir /var/run/sshd

# Place a realistic sensitive file on the filesystem
RUN mkdir -p /home/nurse_user/documents && \
    echo "DB Backup Credentials\nHost: hospital-db\nUser: hospitaluser\nPass: see IT dept" \
    > /home/nurse_user/documents/db_notes.txt && \
    chown -R nurse_user:nurse_user /home/nurse_user/documents

# Place a flag for the attacker to find
RUN echo "FLAG{hospital_workstation_compromised}" > /root/flag.txt && \
    chmod 600 /root/flag.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22

ENTRYPOINT ["/entrypoint.sh"]