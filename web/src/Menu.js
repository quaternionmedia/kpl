import m from 'mithril'

import { message } from 'alertifyjs'
export function Link() {
  return {
    view: (vnode) => {
      return m('.menu-item', [
        m(m.route.Link, vnode.attrs, vnode.children)
      ])
    }
  }
}

export function Links() {
  return {
    view: vnode => {
      return [
        m(Link, {href:'/flight', id: 'flightLink'}, 'flight'),
        m(Link, {href:'/stats', id: 'statsLink'}, 'stats'),
      ]
    }
  }
}

export function Menu() {
  return {
    view: vnode => {
      return [m(Link, {href: '/'}, m('img.logo#logo', {src: '/static/kpl.svg'})),
      m(Links),]
    }
  }
}

export function Layout() {
  return {
    view: vnode => {
      return m('main.layout', {}, [
        m('nav.menu', {}, m(Menu)),
        m('section', vnode.attrs, vnode.children)
      ])
    }
  }
}