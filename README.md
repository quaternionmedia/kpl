# KPL
##### Kerbal Propulsion Laboratory
Because Kerbal needs more than one screen!

## run with docker

`docker-compose up`

Then visit [localhost:8080](http://localhost:8080)

## run locally

### install
`git clone https://github.com/quaternionmedia/kpl.git`

`cd kpl/`

`pip3 install -e .`

(the -e is optional, but helpful for dev environments)

Install the web dependencies
`./kpl.sh init`

### build
Build the web files

`./kpl.sh build`

### run
Wtih Kerbal and krpc running:

$ `kpl`

Then visit [localhost:8888](http://localhost:8888)

or [localhost:8888/stats](http://localhost:8888/stats)
