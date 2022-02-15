# KPL
##### Kerbal Propulsion Laboratory
Because Kerbal needs more than one screen!

![KPL screenshot](https://images.squarespace-cdn.com/content/v1/5b54f2433e2d096995211b77/1619893912422-LVWRTHBTYR6P3MJM8L6L/kpl.jpg?format=1000w)

## about
**KPL** provides realtime flight information from [Kerbal Space Program](https://www.kerbalspaceprogram.com/) through a websocket subscription, and generates dashboard components, viewable on any networked device!

More information available at [quaternion.media/kpl](https://quaternion.media/kpl)

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
