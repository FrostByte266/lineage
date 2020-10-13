<template>
    <h1>{{ title }}</h1>
</template>

<script>
import axios from 'axios';
import protectedMixin from '../mixins/protectedMixin'
export default {
    name: 'Timelines',
    mixins: [protectedMixin],
    data() {
        return {
            id: null,
            title: null,
            nodes: []

        }
    },
    created () {
        const requestedId = this.$route.params.id
        const timeline = axios.get(`/api/timeline/${requestedId}`)
            .then(res => {
                this.id = res.data.uid
                this.title = res.data.title
                this.nodes = res.data.nodes
            })
    }
}
</script>