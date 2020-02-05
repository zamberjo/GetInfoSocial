# OSINT gathering information bot

## Build
```ARMv8
docker-compose -f stack-service.yaml \
    -f stack-service.armv8.yaml up \
    -d --build --force-recreate
```

```
docker-compose -f stack-service.yaml 
    -d --build --force-recreate
```

## Projects useds:
- https://github.com/decoxviii/karma
- https://github.com/sherlock-project/sherlock
- https://github.com/sundowndev/PhoneInfoga
