# Logger API (flask) + immudb + Grafana

## Architecture

![architecture.png](static%2Farchitecture.png)

### Code organization

- **logger_api/app** - Logger API implemented using flask. Depends on **postgres** and **immudb**
- **logger_api/tests** - Tests for Logger API. Depends on **postgres** and **immudb**
- **grafana** - Grafana configuration. Depends on **prometheus**.
- **prometheus** - Prometheus configuration. Depends on **immudb**.
- **postgres** - Import scripts for postgreSQL

## Running the stack

```bash
docker-compose build
docker-compose up
```

## Running backend tests

Run tests only after running previous docker compose up command to have all the dependencies started.

### Logger API

```bash
docker-compose -f docker-compose.yml run --rm  --entrypoint "python -m pytest tests" logger_api
```

## Logger API
### Authentication
The Logger API uses API keys to authenticate requests. 

You can view and manage demo API keys before running the stack
in [users.csv](postgres%2Fusers.csv), or by adding new users with their API keys directly in PostgreSQL while stack is up.

You can pass the API key in each requests using the request header **api-key**.
```bash
-H "api-key: ef229daa-d058-4dd4-9c93-24761842aec5"
```

Demo API key: **ef229daa-d058-4dd4-9c93-24761842aec5**

### REST API

#### /logs/
- Description: Store batch of log lines
- Method: POST
- Content Type: application/json
- URL Structure: ```http://localhost:5001/logs```
- Parameters:
  - app:String - log source app 
  - device:String - log source device 
  - logs:List[String] - logs
- Example:
```bash
curl -X POST 
-H "api-key: ef229daa-d058-4dd4-9c93-24761842aec5" 
-H "Content-Type: application/json" 
-d '{"app":"demo app", "device":"demo device", "logs":["log 1", "log 2"]}' 
"http://localhost:5001/logs/"
```

#### /logs/count
- Description: Print number of stored logs
- Method: GET
- URL Structure: ```http://localhost:5001/logs/count```
- Example:
```bash
curl -X GET 
-H "api-key: ef229daa-d058-4dd4-9c93-24761842aec5" 
"http://localhost:5001/logs/count"
```

#### /logs/tail
- Description: Print last n logs
- Method: GET
- URL Structure: ```http://localhost:5001/logs/tail```
- Parameters:
  - n:String - number of logs to retrieve 
- Example:
```bash
curl -X GET 
-H "api-key: ef229daa-d058-4dd4-9c93-24761842aec5" 
"http://localhost:5001/logs/tail?n=3"
```

#### /logs/all
- Description: Print history of stored logs.
- Method: GET
- URL Structure: ```http://localhost:5001/logs/all```
- Parameters:
  - app:String - log source app
  - device:String - log source device
  - limit:String - number of logs to return
  - offset:String - id offset
- Example:
```bash
curl -X GET 
-H "api-key: ef229daa-d058-4dd4-9c93-24761842aec5" 
"http://localhost:5001/logs/all?app=demo%20app&device=demo%20device&limit=2"
```

#### /logs/verified/id
- Description: verified log retrieval
- Method: GET
- URL Structure: ```http://localhost:5001/logs/verified/1```
- Parameters:
  - id:Integer - id of log to retrieve and verify
- Example:
```bash
curl -X GET 
-H "api-key: ef229daa-d058-4dd4-9c93-24761842aec5" 
"http://localhost:5001/logs/verified/1""
```

## Log generator

https://github.com/mingrammer/flog

### Usage

```
docker run -it --rm mingrammer/flog
```

There are useful options. (`flog --help`)

```console
Options:
  -f, --format string      log format. available formats:
                           - apache_common (default)
                           - apache_combined
                           - apache_error
                           - rfc3164
                           - rfc5424
                           - json
  -o, --output string      output filename. Path-like is allowed. (default "generated.log")
  -t, --type string        log output type. available types:
                           - stdout (default)
                           - log
                           - gz
  -n, --number integer     number of lines to generate.
  -b, --bytes integer      size of logs to generate (in bytes).
                           "bytes" will be ignored when "number" is set.
  -s, --sleep duration     fix creation time interval for each log (default unit "seconds"). It does not actually sleep.
                           examples: 10, 20ms, 5s, 1m
  -d, --delay duration     delay log generation speed (default unit "seconds").
                           examples: 10, 20ms, 5s, 1m
  -p, --split-by integer   set the maximum number of lines or maximum size in bytes of a log file.
                           with "number" option, the logs will be split whenever the maximum number of lines is reached.
                           with "byte" option, the logs will be split whenever the maximum size in bytes is reached.
  -w, --overwrite          overwrite the existing log files.
  -l, --loop               loop output forever until killed.
```

## Grafana

### Web Interface

- URL: http://localhost:3000
- username: **admin**
- password: **admin**

Selecting immudb dashboard: **Dashboard -> Services -> immudb**

![grafana.png](static%2Fgrafana.png)

## immudb

### Web Interface

- URL: http://localhost:8080
- username: **immudb**
- password: **password**

![immudb.png](static%2Fimmudb.png)
