import m from 'mithril'
import { Layout } from './Menu'
import { Smoothie } from './Smoothie'
import { Subscriber } from './Subscriber'
import './style.css'
import { flight_chars } from './constants'

export function Home() {
  return {
    view: vnode => {
      return m('#home', {}, 'Kerbal Propulsion Laboratory')
    }
  }
}

export function Stats() {
  let stats
  return {
    oninit: vnode => {
      m.request('/stats').then(res => {
        console.log('stats', res)
        stats = JSON.stringify(res)
      })
    },
    view: vnode => {
      return m('#stats', vnode.attrs, stats)
    }
  }
}

export function Flight() {
  return {
    view: vnode => {
      return m('.grid', {}, [
        flight_chars.map(char => {
          return m('.elem', {}, [
            m('p.label', {}, char),
            m(Subscriber, {name: char}),
          ])
        })
      ])
    }
  }
}

console.log('kpl started!')

m.route(document.body, '/', {
  '/': { render: () => m(Layout, m(Home))},
  '/test': { render: () => m(Layout, m(Smoothie))},
  '/flight': { render: () => m(Layout, m(Flight))},
  '/stats': { render: () => m(Layout, m(Stats))},
})