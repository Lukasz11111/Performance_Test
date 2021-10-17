FROM ubuntu

WORKDIR /app

RUN  apt-get -yq update && \
     apt-get -yqq install ssh ; \ 
     apt-get install openssh-client

RUN apt-get update                              ; \
apt-get -yqq install ssh                        ; \
apt-get install -y wget openssh-server          ; \
apt-get -y install curl                         ; \
apt install python3-pip     -y                  ; \
apt-get install -y chromium-chromedriver  -y    ; \
pip3 install selenium                           ; \           
pip3 install requests                           ; \
pip3 install openpyxl

COPY . /app

ARG  PATH_ARG
ENV  PATH_=$PATH_ARG

CMD ["bash", "start.sh"] 