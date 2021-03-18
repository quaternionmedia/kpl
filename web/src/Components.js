import m from 'mithril'

import { SmoothieChart, TimeSeries } from 'smoothie'

export function Smoothie() {
  let series = new TimeSeries
  let chart
  return {
    oncreate: vnode => {
      chart = new SmoothieChart(vnode.dom)
      chart.addTimeSeries(series, { strokeStyle: 'rgba(0, 255, 0, 1)' })
      chart.streamTo(vnode.dom, 50)
      setInterval( () => {
      series.append(Date.now(), Math.random() * 10000);
    }, 500)
    },
    view: vnode => {
      return m('canvas', {})
    }
  }
}