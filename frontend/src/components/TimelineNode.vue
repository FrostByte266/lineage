<template>
    <div>
        <h1>{{ title }}</h1>
        <p> {{ content }}</p>
        <img v-if="typeof attachment !== 'undefined'" src="{{ attachment }}">
    </div>
</template>

<script>
export default {
    name: 'TimelineNode',
    props: {
        title: String,
        content: String,
        attachment: String
    }
}
</script>