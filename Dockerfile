FROM balenalib/raspberry-pi-debian-python AS base
RUN git clone https://github.com/mad-ops/stream_sniper.git
WORKDIR /stream_sniper

ENV VIRTUAL_ENV=/stream_sniper/venv
RUN python3 -m virtualenv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3 -m pip install -r requirements.txt

CMD [ "python3", "sniper.py" ]