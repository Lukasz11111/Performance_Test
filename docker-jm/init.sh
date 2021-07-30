test_file="$2"
slave_count="$1"
# sudo docker build -t jmbase .
# sudo docker build -t jm-master jm-master/
# sudo docker build -t jm-slave jm-slave/

sudo docker run -dit --name slave0  jm-slave:latest /bin/bash
sudo docker run -dit --name slave1  jm-slave:latest /bin/bash
sudo docker run -dit --name slave2  jm-slave:latest /bin/bash
sudo docker run -dit --name slave3  jm-slave:latest /bin/bash
sudo docker run -dit --name slave4  jm-slave:latest /bin/bash
sudo docker run -dit --name slave5  jm-slave:latest /bin/bash
# sztywny path!!!!!!!!!!!
sudo docker run -dit --name master -v /home/azureuser/stress_test/test/:/testJM jm-master:latest

sudo touch iphost.txt
sudo chmod 777 iphost.txt
sudo docker inspect --format '{{ .Name }} => {{ .NetworkSettings.IPAddress }}' $(sudo docker ps  -q)  > iphost.txt

iphost=$( python get_hostip_slave.py $slave_count 2>&1) 
echo $iphost

cp $test_file test/test.jmx 

docker exec  master /bin/bash -c "bash /testJM/start.sh $iphost"

sudo docker rm  slave0  -f
sudo docker rm  slave1  -f
sudo docker rm  slave2  -f
sudo docker rm  slave3  -f
sudo docker rm  slave4  -f
sudo docker rm  slave5  -f
sudo docker rm  master  -f

sudo rm  test/test.jmx 

sudo rm iphost.txt
