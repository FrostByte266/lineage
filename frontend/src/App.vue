<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title @click="$router.push('/')">Lineage</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn to="/sanity">Sanity</v-btn>
      </v-toolbar-items>
      <v-toolbar-items v-if="$store.getters.isLoggedIn">
        <v-btn to="/timelines">My Timelines</v-btn>
        <v-btn @click="$store.dispatch('logout')">Logout</v-btn>
      </v-toolbar-items>
      <v-toolbar-items v-else>
        <v-btn to='/register'>Sign Up</v-btn>
        <v-btn to='/login'>Login</v-btn>
      </v-toolbar-items>
    </v-app-bar>

    <v-main>
      <v-container>
        <FlashMessage :position="'right bottom'"></FlashMessage>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data() {
    return {
     routes: []
    }
  },
  created() {
    this.$router.options.routes.forEach(route => this.routes.push(route))
  }
}

</script>
