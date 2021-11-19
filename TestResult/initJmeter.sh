test_file="$1"
slave_count="$2"

sudo touch iphost.txt
sudo chmod 777 iphost.txt
sudo docker inspect --format '{{ .Name }} => {{ .NetworkSettings.IPAddress }}' $(sudo docker ps  -q)  > iphost.txt

iphost=$( python3 get_hostip_slave.py $slave_count 2>&1) 
sudo rm iphost.txt
echo $iphost


sudo cp ../$test_file test.jmx 

sudo docker exec  master /bin/bash -c "bash /testJM/start.sh $iphost"

sudo rm  test.jmx 

