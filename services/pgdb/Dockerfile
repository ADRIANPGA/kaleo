 
FROM postgres:17

# Install necessary packages
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        git \
        postgresql-server-dev-17 && \
    rm -rf /var/lib/apt/lists/*

# Clone and install pgvector
RUN git clone --branch v0.8.0 https://github.com/pgvector/pgvector.git /tmp/pgvector && \
    cd /tmp/pgvector && \
    make && \
    make install && \
    rm -rf /tmp/pgvector