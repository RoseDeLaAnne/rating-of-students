<template>
    <router-link to="/" class="brand">
        <img src="@/media/images/logo.png" alt="" class="brand__icon">
        <div class="brand__name">angela</div>
    </router-link>
</template>

<style lang="sass" scoped>
@import @/styles/keyframes
@import @/styles/mixins
@import @/styles/transitions
@import @/styles/variables



.brand
    display: flex

    align-items: center

    column-gap: 10px

.brand__icon
    width: 64px
    height: 64px

    animation: brand__icon 1.25s ease-in-out infinite alternate

.brand__name
    display: none

    font-size: 24px
    font-weight: 300
</style>