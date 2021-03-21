import m from 'mithril'
import { Connection } from 'autobahn'
import { opts } from './Smoothie'
import { SmoothieChart, TimeSeries } from 'smoothie'
import { flight_chars, flight_types } from './constants'

var connection = new Connection({
  url: 'ws://' + document.location.host + '/ws',
  realm: 'realm1'
})

connection.onopen = function (session) {

   
}

connection.open()

export function Subscriber() {
  let chart
  let series
  let dimensions
  return {
    oninit: vnode => {
      if (vnode.attrs.name in flight_types) {
        dimensions = flight_types[vnode.attrs.name]
        series = []
        for (var i =0; i<dimensions;i++) {
          series.push(new TimeSeries)
        }
      } else {
        dimensions = 1
        series = new TimeSeries
      }
    },
    oncreate: vnode => {
      chart = new SmoothieChart(opts)
      if (dimensions > 1) {
        for (var i =0; i<dimensions;i++) {
          chart.addTimeSeries(series[i], { strokeStyle: `rgba(${i % 3 == 0 ? 255 : 0}, ${i == 1 ? 255 : 0}, ${i > 1 ? 255 : 0}, 1)` })
        }
      } else {
        chart.addTimeSeries(series, { strokeStyle: 'rgba(0, 255, 0, 1)' })
      }
      connection.session.subscribe('local.ksp.' + vnode.attrs.name, args => {
        // console.log(vnode.attrs.name, args[0])
        let data = args[0]
        let t = new Date().getTime()
        if (typeof(data) == typeof([])) {
          for (var i =0; i<dimensions;i++) {
            series[i].append(t, data[i])
        } 
      }
      else {
        series.append(t, args[0])
      }
    })
      chart.streamTo(vnode.dom, 5)
    },
    view: vnode => {
      return m('canvas')
    }
  }
}

