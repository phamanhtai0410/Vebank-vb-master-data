
# **Vebank SYNC MASTER DATA**

<p> => User for syncing the latest data from protocol to BE </p>

## Environment
- docker
- docker-compose

## Notes
- Changes in docker-compose.yml: exposed port, image name, container name
- Changes in supervisord.conf: log files' location

## Use with docker, docker-compose
JUST RUN: `> docker-compose up -d --build`

## Health check
```curl -i <prefix>/common/health_check```

## Container env config:
```/webapps/.env```

## Release v1.0 
