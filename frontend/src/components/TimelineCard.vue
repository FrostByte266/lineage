<template>
    <v-card elevation="2" outlined @click="$router.push({name: 'Timeline', params: {id: uid}})">
        <v-card-title>{{ title }}</v-card-title>
        <v-card-subtitle>Size: {{numNodes}} nodes</v-card-subtitle>
    </v-card>
</template>

<script>
export default {
    name: 'TimelineCard',
    props: {
        title: String,
        numNodes: Number,
        uid: Number
    }
}
</script>