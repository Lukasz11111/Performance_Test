
from opensearchpy import OpenSearch



HOST="18.184.234.115"
PROTOCOL="http"


DBNAME=operationOnConfigPython.getRdbDB(idTest, idMod)
USER=operationOnConfigPython.getRdbDBUser(idTest, idMod)
PASSWORD=operationOnConfigPython.getRdbDBPass(idTest, idMod)

SSH_PKEY="/home/ubuntu/lm_performance_test/TestStart/server1.pem"
PORT=9200


DB_HOST=os.getenv('IP_REMOTE_RDB_DB')
KEY_PW=operationOnConfigPython.getRdbDBSysUser(idTest, idMod)


StartTime=operationOnResult.getStartTime()

def singleOperationOpen(query):
    client = OpenSearch(
        hosts = [{'host': HOST, 'port': PORT}],
        http_compress = True, # enables gzip compression for request bodies
        http_auth = auth,
        # client_cert = client_cert_path,
        # client_key = client_key_path,
        use_ssl = True,
        verify_certs = True,
        ssl_assert_hostname = False,
        ssl_show_warn = False,
        ca_certs = SSH_PKEY
    )




def getTRACE(is_err):
    getall=True
    i=0
    result2=-1
    while getall:
        result = singleOperation(f'''(SELECT COUNT(*) FROM public."segment"  WHERE is_error={is_err} );''')
        time.sleep(5)
        result2 = singleOperation(f'''(SELECT COUNT(*) FROM public."segment"  WHERE is_error={is_err} );''')
        if(result==result2):
            getall=False
        if(i==60):
            result2="Oh, something went wrong"
            getall=False
        i=i+1
    return result2