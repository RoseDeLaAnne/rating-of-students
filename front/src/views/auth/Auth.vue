<template>
    <div class="page">
        <section class="splash">
            <img src="@/media/images/splash.jpg" alt="" class="splash__image">
            <div class="splash__overlay"></div>
        </section>
        <main class="main">
            <div class="main__inner">
                <h1 class="main__title">Аутентификация</h1>
                <h2 class="main__subtitle">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Harum, repudiandae!</h2>

                <form @submit.prevent="Submit" class="form">
                    <div class="input">
                        <div class="input__placeholder">
                            Имя пользователя
                            <svg><use href="@/media/icons/sprites.svg#user" /></svg>
                        </div>
                        <input v-model="username" type="text" :class="{ '--wrong' : isWrong }" @mouseenter="Wrong" placeholder="sokolova">
                    </div>
                    <button class="form__button">Продолжить</button>
                </form>
            </div>
        </main>


        <Loader :active="loaderActive" />
        <!-- <div class="pop">
            <svg class="pop__icon">
                <use href="@/media/icons/sprites.svg#heart" />
            </svg>
            <div class="pop__value">Необходимо ввести имя пользователя</div>
        </div> -->
    </div>
</template>

<script>
import { GET } from '@/utils/fetch.js'


import Loader from '@/components/Loader.vue'



export default {
    name: 'Auth',
    components: {
        Loader
    },
    data() {
        return {
            username: '',

            loaderActive: false,
            isWrong: false,
        }
    },
    created() {
        document.title = 'Аутентификация'
    },
    mounted() {},
    methods: {
        Wrong() {
            this.isWrong = false
        },
        async Submit() {
            const url = `check-student/${this.username.toLowerCase()}`

            if (this.username) {
                const response = await GET(url)

                if (response.status === 200) {
                    localStorage.setItem('username', this.username.toLowerCase())
                    localStorage.setItem('type', 'student')

                    this.$router.push('/auth/confirm')
                } else if (response.status === 404) {
                    const url = `check-professor/${this.username.toLowerCase()}`

                    const response = await GET(url)

                    if (response.status === 200) {
                        localStorage.setItem('username', this.username.toLowerCase())
                        localStorage.setItem('type', 'professor')

                        this.$router.push('/auth/confirm')
                    } else if (response.status === 404) {
                        const url = `check-user/${this.username.toLowerCase()}`

                        const response = await GET(url)

                        if (response.status === 200) {
                            localStorage.setItem('username', this.username.toLowerCase())
                            localStorage.setItem('type', 'user')

                            this.$router.push('/auth/confirm')
                        } else if (response.status === 500) {
                            localStorage.setItem('username', this.username.toLowerCase())
                            localStorage.setItem('type', 'none')

                            this.$router.push('/auth/confirm')
                        }
                    }
                }
            } else {
                this.isWrong = true
            }
        },
    },
}
</script>

<style lang="sass" scoped>
@import @/styles/keyframes
@import @/styles/mixins
@import @/styles/transitions
@import @/styles/variables



.page
    display: flex

    min-height: 100vh

.splash
    position: relative

    width: 55%


    @include MediaW(1440px)
        width: 50%

    @include MediaW(768px)
        position: absolute

        top: 0
        left: 0

        width: 100%

.main
    padding: 0

    width: 45%


    @include MediaW(1440px)
        width: 50%

    @include MediaW(768px)
        width: 100%

.splash__image
    width: 100%
    height: 100vh

.splash__overlay
    position: absolute

    top: 0
    left: 0

    width: 100%
    height: 100%

    background-color: rgba(#000, .05)

.main
    padding: 5%

    display: flex
    flex-direction: column

    align-items: center
    justify-content: center

    text-align: center

    @include MediaW(768px)
        padding: 20px

    @include MediaW(425px)
        padding: 10px

.main__inner
    @include MediaW(768px)
        padding: 5%

        background-color: rgba(#fff, .9)
        box-shadow: 0 5px 10px rgba(#fff, .25)

        z-index: 100

    @include MediaW(425px)
        padding: 7.5% 5%

.main__title
    margin-bottom: 10px

    font-size: 32px
    font-weight: 400


    @include MediaW(1440px)
        font-size: 28px

    @include MediaW(1024px)
        font-size: 24px

    @include MediaW(768px)
        font-size: 28px

    @include MediaW(425px)
        font-size: 20px

.main__subtitle
    margin-bottom: 17.5%

    font-size: 16px


    @include MediaW(1440px)
        font-size: 14px

    @include MediaW(1024px)
        font-size: 12px
    
    @include MediaW(768px)
        font-size: 14px

    @include MediaW(425px)
        font-size: 10px

.form
    width: 100%

    display: flex
    flex-direction: column

.input
    margin-bottom: 32px

    width: 100%

    position: relative

.input__placeholder
    position: absolute

    top: 12px
    left: 16px

    display: flex
    align-items: center

    column-gap: 5px

    font-size: 10px

    color: #888

    
    svg
        min-width: 12px
        width: 12px
        min-height: 12px
        height: 12px

        fill: #888


    @include MediaW(1440px)
        font-size: 8.75px

    @include MediaW(1024px)
        font-size: 7.5px

    @include MediaW(768px)
        font-size: 8.75px

    @include MediaW(425px)
        font-size: 7.5px

.input
    input
        padding: 40px 16px 16px

        width: 100%

        font-size: 14px

        background-color: #fff
        box-shadow: 0 5px 10px rgba(#000, .1)

        transition: box-shadow .5s ease-in-out


        &:focus
            box-shadow: 0 5px 10px rgba(#000, .2)

        &:hover
            box-shadow: 0 5px 10px rgba(#000, .3)

        &.--wrong
            box-shadow: 0 5px 10px rgba(red, .3)



        @include MediaW(1440px)
            font-size: 12.25px

        @include MediaW(1024px)
            font-size: 10.5px

        @include MediaW(768px)
            font-size: 12.25px

        @include MediaW(425px)
            font-size: 10px

.form__button
    width: 100%
    height: 48px

    display: flex

    align-items: center
    justify-content: center

    font-size: 14px

    color: #999
    background-color: #222
    box-shadow: 0 5px 10px rgba(#222, .1)

    transition: color .5s ease-in-out, background-color .5s ease-in-out, box-shadow .5s ease-in-out


    &:hover
        color: #fff
        background-color: #000
        box-shadow: 0 5px 10px rgba(#000, .2)


    @include MediaW(1440px)
        font-size: 12.25px

    @include MediaW(1024px)
        font-size: 10.5px
    
    @include MediaW(768px)
        font-size: 12.25px

    @include MediaW(425px)
        font-size: 10px

// .pop
//     padding: 16px 32px

//     position: fixed

//     bottom: 32px
//     left: 50%

//     transform: translate(-50%, 0)

//     display: flex
//     flex-direction: column

//     align-items: center

//     background-color: #fff

// .pop__icon
//     margin-top: -48px
//     margin-bottom: 24px

//     width: 64px
//     height: 64px

//     fill: red
</style>
