<template>
    <div class="modal">
        <!-- Loader -->
    </div>
</template>

<script>
import { JWTDecode } from '@/utils/jwt.js'
import { SetCookie, DeleteCookie, GetCookie } from '@/utils/cookie.js'
import { POST, GET } from '@/utils/fetch.js'



export default {
    name: 'Modal',
    props: {},
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



// 
</style>
