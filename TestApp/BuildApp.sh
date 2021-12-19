
idTest=$1
idMod=$2
whatStart=$3


KEY="$(python3 operationOnConfig.py -getKeyPathApp $1 -mod $2 2>&1)"
REMOTE_HOST="$(python3 operationOnConfig.py -getAppHost $1 -mod $2 2>&1)"
USER_SYSTEM="$(python3 operationOnConfig.py -getUserAppSys $1 -mod $2 2>&1)"
APP_PATH="$(python3 operationOnConfig.py -getAppPath $1 -mod $2 2>&1)"
APP_DIR="$(python3 operationOnConfig.py -getAppDir $1 -mod $2 2>&1)"

function build(){
    python3 $APP_SERVER_FILE_PATH/CreateEnv.py  $idTest $idMod a
    sleep 1
    env="$(cat $APP_SERVER_FILE_PATH.env)"

    
    bashCommand='cd ~/'$APP_PATH'/'$APP_DIR';
    sudo docker-compose down;
    sleep 2;
    sudo rm .env;
    sleep 2;
    echo "'$env'" > .env;
    sleep 12;
    sudo docker-compose build --no-cache;
    sleep 15;
    sudo docker-compose up -d;
    '
echo $bashCommand

    . RemoteServer.sh $KEY $REMOTE_HOST $USER_SYSTEM "$bashCommand"
    sleep 160
    echo App build and start
}

function buildDataGeneration(){
    
    python3 $APP_SERVER_FILE_PATH/CreateEnv.py  $idTest $idMod no-version
    sleep 1
    env="$(cat $APP_SERVER_FILE_PATH.env)"
    GEN_DIR="$(python3 operationOnConfig.py -getAppGenDataDir $idTest -mod $idMod 2>&1)"

    bashCommand='cd '$APP_PATH'/'$GEN_DIR';
    sudo docker-compose down;
    sudo rm .env;
    sleep 2;
    echo "'$env'" > .env;
    sleep 12;
    sudo docker-compose build --no-cache;
    sleep 12;
    sudo docker-compose up -d;
    '
    echo $bashCommand
    . RemoteServer.sh $KEY $REMOTE_HOST $USER_SYSTEM "$bashCommand"
    sleep 160
    echo App build and start
}


if [[ $whatStart == "gen" ]]; then
    buildDataGeneration 
fi

if [[ $whatStart == "app" ]]; then
    build 
fi