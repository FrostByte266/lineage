<template>
    <v-flex d-flex>
        <v-layout wrap>
            <v-flex ml-4 class="ma-5" v-for="timeline in timelines" :key="timeline.uid">
                <TimelineCard :title="timeline.title" :numNodes="timeline.nodes.length" :uid="timeline.uid" />
            </v-flex>
        </v-layout>
    </v-flex>
</template>

<script>
import TimelineCard from '../components/TimelineCard'
export default {
    name: 'TimelineGrid',
    components: {
        TimelineCard
    },
    props: {
        timelines: Array[Object]
    }
}
</script>