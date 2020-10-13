<!-- <template>
    <v-container>
        <v-col>
            <v-row><TimelineCard>Example</TimelineCard></v-row>
        </v-col>
    </v-container>
</template> -->

<template>
    <TimelineGrid :timelines="timelines" />
</template>

<script>
import protectedMixin from '../mixins/protectedMixin'
import TimelineGrid from '../components/TimelineGrid'
import axios from 'axios'
export default {
    name: 'Timelines',
    mixins: [protectedMixin],
    data () {
        return {
            timelines: []
        }
    },
    components: {
        TimelineGrid
    },
    created() {
        axios.get('/api/timelines')
            .then((res) => this.timelines = res.data)
            .catch(err => console.error(err))
    }

}
</script>