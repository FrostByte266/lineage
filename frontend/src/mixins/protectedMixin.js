import axios from 'axios'
export default {
    created() {
        axios.get('/api/login')
            .catch(e => {
                const login_href = this.$router.resolve({name: 'Login', query: {next: this.$route.path}}).href
                console.log(login_href)
                if(this.$store.getters.isLoggedIn) {
                    this.flashMessage.error({
                        title: 'Your session has expired, please log back in!'
                    })
                    this.$store.dispatch('logout')
                } else {
                    this.flashMessage.error({
                        title: 'You must be logged in to view this page!'
                    })
                }
                this.$router.push(login_href)
            })
    }
}