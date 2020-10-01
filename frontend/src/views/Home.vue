<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <h1 v-if="loggedIn"> Welcome {{ currentUser }}</h1>
    <h1 v-else>Please log in</h1>
  </div>
</template>

<script>
export default {
  name: 'Home',
  computed: {
    loggedIn() {
      return this.$store.getters.isLoggedIn
    },
    currentUser() {
      return this.$store.getters.currentUser
    }
  }
}
</script>
