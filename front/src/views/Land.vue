<template>
    <div class="page">
        <div class="wrapper">
            <main class="main">
                Land Page
            </main>
        </div>
    </div>
</template>

<script>
import { JWTDecode } from '@/utils/jwt.js'
import { SetCookie, DeleteCookie, GetCookie } from '@/utils/cookie.js'
import { POST, GET } from '@/utils/fetch.js'



export default {
    name: 'Land',
    data() {
        return {}
    },
    created() {
        // document.title = 'Title'
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



// 
</style>
