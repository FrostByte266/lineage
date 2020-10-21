<template>
    <v-timeline-item>
        <v-card>
            <v-card-title>{{ title }}</v-card-title>
            <v-card-text>{{ content }}</v-card-text>
            <v-img v-if="attachment !== null" :src="attachment" />
        </v-card>
    </v-timeline-item>
</template>

<script>
export default {
    name: 'TimelineNode',
    props: {
        title: String,
        content: String,
        attachment: String
    },
    created() {
        alert(this.attachment !== null)
    }
}
</script>