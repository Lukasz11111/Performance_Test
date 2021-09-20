# Performance tests RevDeBug

The script is used to send a large number of requests to selected applications that use RvDeBug in order to test as an application with RevDebug and the Revdebug instance itself will behave under heavy load.
## Init script
## Using test
### Application
The first step to run the tests is to create a test application with at least 2 endpoints: endpoint with error and endpoint with success.

In order to compare the operation of the application with DevOps and APM, with DevOps only, with APM only and with the application without RevDeBug, applications should be launched in four instances.

### Config
After creating and running the application, create a folder in the Application folder with the .config file
```
Application/your_app/.config
```

```
{
"active": "true",
"test_time":"15",
"git_link":"",
"application_name": "PythonFlask",
"server_rdb": "20.199.127.147",
"language":"py",
"info":"rdb and apm",
"cpu": "8",
"ram": "32",
"size": "1024",
"err":"err",
"success":"/",
"protocol":"http",
"delay": "0 10",
"raport_name": "Performance_test_after_changes",
"proportions":{
"100":"0",
"95":"0",
"90":"0",
"85":"0",
"80":"0",
"75":"0",
"70":"0",
"65":"0",
"60":"0",
"55":"0",
"50":"0",
"45":"0",
"40":"0",
"35":"0",
"30":"0",
"25":"0",
"20":"0",
"15":"0",
"10":"0",
"5":"0",
"0":"1"
},
"module": {
    "rdb_and_apm":{
        "is_on":"True",
        "host":"40.89.147.34",
        "port":"8223"
    },
    "apm":{
        "is_on":"false",
        "host":"40.89.147.34",
        "port":"8224"
    },
    "none":{
        "is_on":"false",
        "host":"40.89.147.34",
        "port":"8225"
    },
    "rdb":{
        "is_on":"false",
        "host":"40.89.147.34",
        "port":"8210"
    }
}
}
```
Specifies whether the test from the file will  be performed or skipped
```
"active": "true",
``` 
Determines the time of a single test rune in jmeter  (in seconds)
```
 "test_time":"15",
```
Information for the report
```
"git_link":"", 
"language":"py",
"info":"rdb and apm",
"cpu": "8",
"ram": "32",
"size": "1024", 
```
Name of the application in RevDeBug
```
"application_name": "PythonFlask", 
```
RevDeBug instance
```
"server_rdb": "20.199.127.147",
```
Endpoint ending with an error (/error)
```
"err":"error",  
```
Successful endpoint
```
"success":"/",
```
Delay in calling up enpoints by jmeter. Affects the number of calls per second. Enter the consecutive delay numbers after the space. Each occurrence of a delay equals +1 to each of the test runs
```
"delay": "0 10",
```
Proportion of the number of successful endpoint calls to failed endpoints (100 - 100% success, 0 - 100% error) Assign: 0 - not performed, 1 - performed. Each occurrence of a proportion is 1+ to all test runs
```
"proportions":{                           
"100":"0",
"95":"0",
"90":"0",
"85":"0",
"80":"0",
"75":"0",
"70":"0",
"65":"0",
"60":"0",
"55":"0",
"50":"0",
"45":"0",
"40":"0",
"35":"0",
"30":"0",
"25":"0",
"20":"0",
"15":"0",
"10":"0",
"5":"0",
"0":"1"
},
```
Applications to which jmeter will send requests
```
"rdb_and_apm":{
        ...
    },
```
Determining whether the jemteter is to send requests for applications with the given modules
```
 "is_on":"True",
```
Application host
```
 "host":"40.89.147.34",
```
Application port
```
 "port":"8223"
```

### Script start
After configuration, to run the test, start docker-compose in the main directory
```
sudo docker-compose up -d; sudo docker-compose logs tail=100 -f
```
After the run, the test will generate a report in .xlsx format in the reports directory