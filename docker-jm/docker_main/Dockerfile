FROM ubuntu

RUN apt-get update;apt-get install -y wget openssh-server

COPY . /

CMD ["bash", "/start.sh"]