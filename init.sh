
    # 1. Installing required applications
    sudo apt-get update
    sudo apt-get -y install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common

    # 2. Adding docker repository
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    sudo add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
       $(lsb_release -cs) \
       stable"

    # 3. Installing latest docker
    sudo apt-get update
    sudo apt-get -y install docker-ce docker-ce-cli containerd.io


    # 4. Installing docker-compose

    sudo apt-get update
    sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    # 5. Install Java JRE

    sudo apt-get install openjdk-8-jre

    # 6. Install Jmeter

    mkdir jmeter
    cd jmeter
    wget http://www.gtlib.gatech.edu/pub/apache/jmeter/binaries/apache-jmeter-5.4.tgz
    tar -xf apache-jmeter-5.4.tgz

    # 7. Install cypress dependencies
    sudo apt-get install libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2 libxtst6 xauth xvfb

    # 8. Install python module
    sudo apt install python3-pip
    pip install openpyxl