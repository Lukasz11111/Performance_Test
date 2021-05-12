# Use Java 8 slim JRE
FROM openjdk:8-jre-slim
MAINTAINER TestAutomationGuru

# JMeter version
ARG JMETER_VERSION=5.4.1

# Install few utilities
RUN apt-get clean && \
    apt-get update && \
    apt-get -qy install \
                wget \
                telnet \
                iputils-ping \
                unzip

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