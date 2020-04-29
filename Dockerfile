###Linux Things
FROM balenalib/raspberry-pi-debian-python:3.7-latest-build AS base
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y flock

###Git Things
WORKDIR /usr/
RUN git clone https://github.com/mad-ops/stream_sniper.git app
RUN git pull
WORKDIR /usr/app

###Python Things
ENV VIRTUAL_ENV=/venv
RUN python3 -m pip install virtualenv
RUN python3 -m virtualenv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3 -m pip install -r requirements.txt

###CRON Things

#Let's go!
CMD [ "python3", "sniper.py", "moonmoon" ]