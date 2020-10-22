import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store/index'

import Home from '../views/Home'
import Login from '../views/Login'
import Register from '../views/Register'
import Timelines from '../views/Timelines'
import Timeline from '../views/Timeline'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/timelines',
    name: 'Timelines',
    meta: {
      requiresAuth: true
    },
    component: Timelines
  },
  {
    path: '/timeline/:id',
    name: 'Timeline',
    meta: {
      requiresAuth: true
    },
    component: () => Timeline
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  const url = router.resolve({name: 'Login', query: {next: to.path}})
  if(to.matched.some(record => record.meta.requiresAuth)) {
    if (router.app.$store.getters.isLoggedIn) {
      next()
    } else {
      next(url)
    }
  } else {
    next()
  }
})

export default router
