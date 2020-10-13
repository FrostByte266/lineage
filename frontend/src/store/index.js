import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: localStorage.getItem('token') || '',
    user: ''
  },
  mutations: {
    authSuccess(state, {token, user}){
      state.token = token
      state.user = user
    },
    authLogout(state){
      state.token = ''
      state.user = ''
    }
  },
  actions: {
    login({commit}, user){
      return new Promise((resolve, reject) => {
        axios({url: '/api/login', data: user, method: 'POST'})
        .then(res => {
          const token = res.data.token
          const user = res.data.username
          localStorage.setItem('token', token)
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
          commit('authSuccess', {token, user})
          resolve(res)
        })
        .catch(err => {
          localStorage.removeItem('token')
          reject(err)
        })
      })
    },
    register({commit}, user){
      return new Promise((resolve, reject) => {
        axios({url: '/api/register', data: user, method: 'POST'})
        .then(res => {
          console.log(res)
          const token = res.data.token
          const user = res.data.username
          localStorage.setItem('token', token)
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
          commit('authSuccess', {token, user})
          resolve(res)
        })
        .catch(err => {
          localStorage.removeItem('token')
          reject(err)
        })
      })
    },
    logout({commit}){
      return new Promise((resolve, reject) => {
        commit('authLogout')
        axios.delete('/api/login')
          .then(res => {
            localStorage.removeItem('token')
            delete axios.defaults.headers.common['Authorization']
            resolve()
          }).catch(e => {
            console.error(e)
            reject(e)
          })
      })
    }
  },
  modules: {
  },
  getters: {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    currentUser: state => state.user
  }
})
