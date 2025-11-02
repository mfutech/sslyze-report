# Keep track of your TLS end point certificates and TLS configuration

a simple scanner, database and webgui to keep track of your TLS/SSL web server or other end point configuration.
provide a quick overview on 

* which certicate and going to exprire but as still in use.
* whatever the TLS configuration is secure (accoding to mozilla standard)


# tech stack
currently
* python
* sqlite
* vue.js

uses sslyze from https://github.com/nabla-c0d3/sslyze to scan and analyse TLS and certificate configuraiton.

# status

in development, PR, Bug Reports, improvement proposal welcomed.

# installation

## pre-requisite
```
install sqlite3 if not present
```

## installation
```
clone repo
cd repo
cp config.ini.example config.ini
customize section hostlist
cd client
fnm use ## or you prefered node version manager
npm install
cd ..
./db_migration.bash
uv run build-client
uv run tomlscript waitress
```

## runing a scan

otherwise you will not ave much data

make sure te config.ini hostlist section is populated with the host you want to monitor

```
uv run python scan.py
```
