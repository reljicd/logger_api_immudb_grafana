# Logger API (flask) + immudb + Grafana

## Architecture

![architecture.png](static%2Farchitecture.png)

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

https://github.com/codenotary/immudb

### Web Interface

- URL: http://localhost:8080
- username: **immudb**
- password: **password**

![immudb.png](static%2Fimmudb.png)