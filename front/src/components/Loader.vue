<template>
    <div class="loader" :class="{'--active': active }">
        <div class="loader__decor"></div>
        <div class="loader__title">Загрузка</div>
    </div>
</template>

<script>
export default {
    name: 'Loader',
    components: {
    },
    props: {
        active: Boolean
    },
    data() {
        return {}
    },
    methods: {}
}
</script>

<style lang="sass" scoped>
@import @/styles/keyframes
@import @/styles/mixins
@import @/styles/transitions
@import @/styles/variables




.loader
    position: fixed

    top: 0
    left: var(--barWidth)

    width: calc(100% - var(--barWidth))
    height: 100vh

    display: flex
    flex-direction: column

    align-items: center
    justify-content: center

    row-gap: 50px

    visibility: hidden
    opacity: 0

    // animation: loader .5s ease-in-out
    transition: background-color .5s ease-in-out, visibility .5s ease-in-out, opacity .5s ease-in-out

    z-index: 100


    &.--active
        background-color: rgba(#000, .75)

        visibility: visible
        opacity: 1

    
    @include MediaW(1024px)
        left: 0

        width: 100%

.loader__decor
    position: relative

    width: 350px
    height: 350px


    &:before,
    &:after
        content: ''

        position: absolute

        top: 0
        left: 0

        width: 350px
        height: 350px

    &:before
        background: linear-gradient(90deg, rgba(#ff930f, .5) 0%, rgba(#fff95b, .5) 100%)

        animation: access__decor 10s ease-in-out infinite alternate

    &:after
        background: linear-gradient(90deg, rgba(#ff0f7b, .6) 0%, rgba(#f89b29, .6) 100%)

        animation: access__decor 5s ease-in-out infinite alternate

.loader__title
    font-size: 32px
    font-weight: 300

    text-align: center

    text-transform: uppercase

    letter-spacing: .6em

    white-space: nowrap

    color: #FFF
</style>
