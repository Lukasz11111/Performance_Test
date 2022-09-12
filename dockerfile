FROM ubuntu

WORKDIR /app

RUN  apt-get -yq update && \
     apt-get -yqq install ssh ; \ 
     apt-get install openssh-client


RUN apt-get update                              ; \
apt-get -yqq install ssh                        ; \
apt-get install -y wget openssh-server          ; \
apt-get -y install curl                         ; \
apt-get install python3-pip     -y              ; \
# apt-get -y install google-chrome-stable          ; \
# apt-get install -y chromium-browser             ; \
# apt-get install -y chromium-chromedriver        ; \
# apt-get install -y urllib3                       ; \
pip3 install selenium                           ; \           
pip3 install requests                           ; \
pip3 install openpyxl                            ; \
pip3 install sshtunnel                            ; \
pip3 install gspread                            ; \
pip3 install gspread_formatting                            ; \
pip3 install psycopg2-binary                      ; \
pip install opensearch-py

# RUN apt-get install -y libglib2.0-0 \
#     libnss3 \
#     libgconf-2-4\
#     libfontconfig1

COPY . /app

RUN bash instalSelenium.sh

RUN pip3 install httpx

ARG  PATH_ARG
ENV  PATH_=$PATH_ARG

CMD ["bash", "start.sh"] 