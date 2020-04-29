FROM balenalib/raspberry-pi-debian-python:3.7-latest-build AS base
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y flock
RUN git clone https://github.com/mad-ops/stream_sniper.git

WORKDIR /stream_sniper
RUN git pull

ENV VIRTUAL_ENV=/venv
RUN python3 -m pip install virtualenv
RUN python3 -m virtualenv $VIRTUAL_ENV
RUN ls
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3 -m pip install -r requirements.txt

CMD [ "python3", "sniper.py", "moonmoon" ]