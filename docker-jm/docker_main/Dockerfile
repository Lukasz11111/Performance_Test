FROM ubuntu

RUN  apt-get -yq update && \
     apt-get -yqq install ssh ; \ 
     apt-get install openssh-client

RUN apt-get update                      ; \
apt-get -yqq install ssh                ; \
apt-get install -y wget openssh-server  ; \
apt-get -y install curl;

ARG PATH_ARG=
ENV PATH_=$PATH_ARG

COPY . /

CMD ["bash", "/start.sh"] 