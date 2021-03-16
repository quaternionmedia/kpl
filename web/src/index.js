import m from 'mithril'
import { Layout } from './Menu'


export function Home() {
  return {
    view: vnode => {
      return m('#home', {}, 'kpl')
    }
  }
}
console.log('kpl started!')

m.route(document.body, '/', {
  '/': { render: () => m(Layout, m(Home))},
})