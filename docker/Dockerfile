FROM python:3.11-slim

MAINTAINER gopro-overlay@time4tea.net
ENV PATH=$PATH:/usr/bin


RUN apt update && apt install -y --no-install-recommends \
        curl \
        gcc \
        gnupg \
        unzip \
        fonts-noto \
        fonts-roboto \
        ffmpeg \
        make \
        libcairo2-dev \
        pkg-config \
        sudo \
	# this should be optional \
        #libnvidia-decode-535-server \
        # libnvidia-encode-535-server \
    && rm -rf /var/lib/apt/lists/* \
    && apt clean

WORKDIR /app
ARG GOPRO_OVERLAY_VERSION

#RUN pip install --no-cache-dir \
#    pycairo==1.23.0 \
#    gopro-overlay==${GOPRO_OVERLAY_VERSION}
    
# COPY entrypoint.sh /app
# ENTRYPOINT [ "/app/entrypoint.sh" ]
