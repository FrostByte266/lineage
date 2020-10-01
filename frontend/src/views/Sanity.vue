<template>
    <h1>{{ message }}</h1>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Sanity',
    data() {
        return { message: '' }
    },
    created() {
        axios.get('/api/sanity')
        .then(response => {
            this.message = response.data
        }).catch(error => console.error(error))
    }
}
</script>