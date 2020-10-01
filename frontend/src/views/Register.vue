<template>
    <v-form ref="form" @keydown.enter="register" @submit.prevent="register">
        <v-row>
            <v-text-field v-model="username" :rules="[notEmptyRule]" label='Username' required></v-text-field>
        </v-row>
        <v-row>
            <v-text-field v-model="password" :rules="[notEmptyRule, passwordsMatchRule]" :append-icon="passwordShown ? 'mdi-eye': 'mdi-eye-off'" :type="passwordShown ? 'text': 'password'" @click:append="passwordShown = !passwordShown" label="Password" required></v-text-field>
        </v-row>
        <v-row>
            <v-text-field v-model="passwordConfirm" :rules="[notEmptyRule, passwordsMatchRule]" :append-icon="passwordConfirmShown ? 'mdi-eye': 'mdi-eye-off'" :type="passwordConfirmShown ? 'text': 'password'" @click:append="passwordConfirmShown = !passwordConfirmShown" label="Password Confirmation" required></v-text-field>
        </v-row>
        <v-row>
            <v-btn color="primary" type="submit">Register</v-btn>
        </v-row>
    </v-form>
</template>

<script>
export default {
    name: 'Register',
    data() {
        return {
            username: '',
            password: '',
            passwordConfirm: '',
            passwordShown: false,
            passwordConfirmShown: false,
            notEmptyRule: e => !!e || 'Input can\'t be blank!',
            passwordsMatchRule: e => this.password === this.passwordConfirm || 'Passwords must match!',
        }
    },
    methods: {
        register() {
            if(this.$refs.form.validate()){
                const data = {
                    username: this.username,
                    password: this.password,
                    passwordConfirm: this.passwordConfirm
                }
                this.$store.dispatch('register', data)
                .then(() => this.$router.push('/'))
                .catch(err => {
                    this.flashMessage.error({
                        title: 'Username taken!',
                        message: 'Please pick a different username.'

                    })
                })
            } else {
                return false
            }
        }
    }
}
</script>


