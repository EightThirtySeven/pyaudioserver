# audioserver

A Python audio server that supports `hermes/audioServer/{siteId}playBytes/{requestId}`.

## Installing
```bash
$ python -m pip install -e ./audioserver

# For macOS
$ python -m pip install pyobjc
```

## Running
```bash
$ python -m audioserver <site_id> --host localhost --port 1883
```