import m from 'mithril'
import { Layout } from './Menu'
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

console.log('kpl started!')

m.route(document.body, '/', {
  '/': { render: () => m(Layout, m(Home))},
  '/stats': { render: () => m(Layout, m(Stats))},
})