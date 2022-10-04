<template>
    <div class="empty">
        <div class="empty__title">{{ title }}</div>
        <div class="empty__subtitle">{{ subtitle }}</div>
    </div>
</template>

<script>
import { JWTDecode } from '@/utils/jwt.js'
import { SetCookie, DeleteCookie, GetCookie } from '@/utils/cookie.js'
import { POST, GET } from '@/utils/fetch.js'



export default {
    name: 'Empty',
    props: {
        title: {
            type: String,
            require: true,
        },
        subtitle: {
            type: String,
            require: true,
        },
    },
    data() {
        return {}
    },
    mounted() {},
    methods: {},
}
</script>

<style lang="sass" scoped>
@import @/styles/keyframes
@import @/styles/mixins
@import @/styles/transitions
@import @/styles/variables



.empty
    display: flex
    flex-direction: column

    align-items: center
    
    row-gap: 12px

    text-align: center

.empty__title
    font-size: 24px

.empty__subtitle
    font-size: 16px
    font-weight: 300
</style>
