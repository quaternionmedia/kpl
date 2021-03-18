import m from 'mithril'
import { Layout } from './Menu'
import { Smoothie } from './Smoothie'
import './style.css'

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
      return m(Smoothie)
    }
  }
}

console.log('kpl started!')

m.route(document.body, '/', {
  '/': { render: () => m(Layout, m(Home))},
  '/flight': { render: () => m(Layout, m(Flight))},
  '/stats': { render: () => m(Layout, m(Stats))},
})