import m from 'mithril'
import { Connection } from 'autobahn'
import { opts } from './Smoothie'
import { SmoothieChart, TimeSeries } from 'smoothie'
import { flight_chars } from './constants'

var connection = new Connection({
  url: 'ws://' + 'localhost:8080' + '/ws',
  realm: 'realm1'
})

connection.onopen = function (session) {

   
}

connection.open()

export function Subscriber() {
  let chart
  let series = new TimeSeries
  
  return {
    oninit: vnode => {
      chart = new SmoothieChart(opts)
      chart.addTimeSeries(series, { strokeStyle: 'rgba(0, 255, 0, 1)' })
      connection.session.subscribe('local.ksp.' + vnode.attrs.name, args => {
        // console.log(vnode.attrs.name, args[0])
        series.append(new Date().getTime(), args[0])
      })
    },
    oncreate: vnode => {
      chart.streamTo(vnode.dom, 5)
    },
    view: vnode => {
      return m('canvas')
    }
  }
}

