<template>
  <div class="home">
    <h1 class="centered">Lineage</h1>
    <h1 class="centered" v-if="loggedIn">
      Welcome {{ currentUser }} <br />
      <router-link to="timelines">View your timelines here</router-link>
    </h1>
    <h1 class="centered" v-else>Please log in</h1>
  </div>
</template>

<script>
export default {
  name: "Home",
  computed: {
    loggedIn() {
      return this.$store.getters.isLoggedIn;
    },
    currentUser() {
      return this.$store.getters.currentUser;
    },
  },
};
</script>

<style scoped>
  .centered {
    text-align: center;
    font-weight: normal;
    font-size: 3em;
  }
</style>
