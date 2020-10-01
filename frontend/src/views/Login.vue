<template>
    <v-form ref="form" @keydown.enter="login" @submit.prevent="login">
        <v-row>
            <v-text-field v-model="username" :rules="notEmptyRule" label='Username' required></v-text-field>
        </v-row>
        <v-row>
            <v-text-field v-model="password" :rules="notEmptyRule" :append-icon="passwordShown ? 'mdi-eye': 'mdi-eye-off'" :type="passwordShown ? 'text': 'password'" @click:append="passwordShown = !passwordShown" label="Password" required></v-text-field>
        </v-row>
        <v-row>
            <v-btn color="primary" type="submit">Login</v-btn>
        </v-row>
    </v-form>
</template>

<script>
export default {
    name: 'Login',
    data() {
        return {
            notEmptyRule: [e => !!e || 'Input can\'t be blank!'],
            username: '',
            password: '',
            passwordShown: false
        }
    },
    methods: {
        login() {
            if(this.$refs.form.validate()){
                const data = {
                    username: this.username,
                    password: this.password
                }
                this.$store.dispatch('login', data)
                .then(() => this.$router.push('/'))
                .catch(error => {
                    this.flashMessage.error({
                        title: 'Invaid credentials',
                        message: 'Please double check your username/password'
                    })
                })
            } else {
                return false
            }
        }
    }
}
</script>


