
    # #  Installing required applications
    # sudo apt-get update
    # sudo apt-get -y install \
    #     apt-transport-https \
    #     ca-certificates \
    #     curl \
    #     gnupg-agent \
    #     software-properties-common

    # #  Adding docker repository
    # curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    # sudo add-apt-repository \
    #    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    #    $(lsb_release -cs) \
    #    stable"

    # #  Installing latest docker
    # sudo apt-get update
    # sudo apt-get -y install docker-ce docker-ce-cli containerd.io


    # #  Installing docker-compose

    # sudo apt-get update
    # sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    # sudo chmod +x /usr/local/bin/docker-compose


    #  Install cypress dependencies
    sudo apt-get install libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2 libxtst6 xauth xvfb
    sudo apt-get install npm
    cd cy
    sudo npm install
    cd ..


    #  Install python module
    sudo apt install python3-pip
    pip install openpyxl
        #  Build img
    sudo docker-compose build
    cd docker-jm
    sudo docker build -t jmbase .
    sudo docker build -t jm-master jm-master/
    sudo docker build -t jm-slave jm-slave/
    cd ..
    mkdir raports
echo DONE