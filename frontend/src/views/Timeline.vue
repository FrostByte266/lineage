<template>
    <div>
        <v-icon class="hover" @click="$router.go(-1)">fa-arrow-left</v-icon>
        <h1>{{ title }}</h1>
        <v-timeline>
            <TimelineNode v-for="node in nodes" :key="node.uid" :title="node.title" :content="node.content" :attachment="node.attachment" />
        </v-timeline>
    </div>
</template>

<script>
import axios from 'axios';
import protectedMixin from '../mixins/protectedMixin'
import TimelineNode from '../components/TimelineNode'
export default {
    name: 'Timelines',
    mixins: [protectedMixin],
    components: {
        TimelineNode
    },
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

<style scoped>
    div >>> .hover:hover {
        transform: translate(-10px, 0px);
    }
</style>