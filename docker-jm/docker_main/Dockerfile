FROM ubuntu

WORKDIR /app

RUN  apt-get -yq update && \
     apt-get -yqq install ssh ; \ 
     apt-get install openssh-client

RUN apt-get update                           ; \
apt-get -yqq install ssh                     ; \
apt-get install -y wget openssh-server       ; \
apt-get -y install curl                     
 

COPY . /app

ARG  PATH_ARG
ENV  PATH_=$PATH_ARG

CMD ["bash", "start.sh"] 