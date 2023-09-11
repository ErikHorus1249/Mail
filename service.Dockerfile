FROM python:3.8.2-slim-buster

ENV TZ="Asia/Ho_Chi_Minh"

WORKDIR /core

RUN apt-get update && apt-get install -y \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    gcc python3-dev musl-dev  \
    libffi-dev netcat vim \ 
    iputils-ping \
    net-tools \
    curl \
    zip 

#  Chrome instalation 
RUN curl -LO  https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
apt-get install -y ./google-chrome-stable_current_amd64.deb && \
rm google-chrome-stable_current_amd64.deb

RUN pip install --upgrade pip

COPY ./driver/chromedriver /usr/bin/

COPY service.requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./core/config/event.py /usr/local/lib/python3.8/site-packages/calendar_view/core/event.py
