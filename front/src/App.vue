<template>
    <router-view />
</template>

<script>
import { JWTDecode } from '@/utils/jwt.js'
import { SetCookie, DeleteCookie, GetCookie } from '@/utils/cookie.js'
import { POST, GET } from '@/utils/fetch.js'



export default {}
</script>

<style lang="sass">
@import @/styles/config
@import @/styles/general
</style>
