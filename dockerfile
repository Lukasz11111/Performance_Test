# Use Java 8 slim JRE
FROM openjdk:8-jre-slim as jmbase

# JMeter version
ARG JMETER_VERSION=5.4.1

# Install few utilities
RUN apt-get update && \
    apt-get -qy install \
                wget \
                telnet \
                iputils-ping \
                unzip \
                python3

# Install JMeter
RUN   mkdir /jmeter \
      && cd /jmeter/ \
      && wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-$JMETER_VERSION.tgz \
      && tar -xzf apache-jmeter-5.4.1.tgz \
      && rm apache-jmeter-5.4.1.tgz

# Set JMeter Home
ENV JMETER_HOME /jmeter/apache-jmeter-5.4.1/

# Add JMeter to the Path
ENV PATH $JMETER_HOME/bin:$PATH

# Use vinsdocker base image
FROM jmbase

# Ports to be exposed from the container for JMeter Master
EXPOSE 60000

WORKDIR /app
COPY run.sh /run.sh
RUN chmod 777 /run.sh


CMD ["/run.sh"]

