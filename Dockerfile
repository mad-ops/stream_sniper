FROM balenalib/raspberry-pi-debian-python AS base
RUN git clone https://github.com/mad-ops/stream_sniper.git
WORKDIR /stream_sniper
RUN pip install -r requirements.txt