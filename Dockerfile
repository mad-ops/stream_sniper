###Linux Things
FROM balenalib/raspberry-pi-debian-python:3.7-latest-build AS base
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install cron
RUN apt-get install ffmpeg

###Git Things
WORKDIR /usr/
RUN git clone https://github.com/mad-ops/stream_sniper.git app
WORKDIR /usr/app

###Python Things
ENV VIRTUAL_ENV=/usr/app/venv
RUN python3 -m pip install virtualenv
RUN python3 -m virtualenv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3 -m pip install -r requirements.txt

###CRON Things
RUN /usr/bin/crontab crontab

#Let's go!
CMD [ "cron", "-f"]