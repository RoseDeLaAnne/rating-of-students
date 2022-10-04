<template>
    <div class="page">
        <!-- <section class="splash">
            <video src="@/media/videos/overlay.mp4" muted loop autoplay class="splash__video"></video>
            <div class="splash__overlay"></div>
        </section>
        <main class="main">
            <h1 class="main__title"></h1>
            <h2 class="main__subtitle"></h2>

            <form @submit.prevent="Submit">
                <div class="user">
                    <section class="user__left">
                        <img src="@/media/images/avatar.png" alt="" class="user__avatar">
                    </section>
                    <section class="user__middle">
                        <input v-model="name" type="text" class="user__title" placeholder="Васильев Никита">
                        <div class="user__subtitle">
                            <div>vasilyev</div>
                            <div>*</div>
                            <input type="text" placeholder="20138">
                        </div>
                    </section>
                    <section class="user__right">
                        <label class="label">
                            <input type="checkbox">
                            <div class="label__checkbox"></div>
                            <div class="label__value">Студент</div>
                        </label>
                        <label class="label">
                            <input type="checkbox">
                            <div class="label__checkbox"></div>
                            <div class="label__value">Доцент</div>
                        </label>
                    </section>
                </div>

                <input v-model="password" type="password" placeholder="ak47coder5">
                <button>Авторизоваться</button>
            </form>
        </main> -->
        <section class="splash">
            <img src="@/media/images/splash.jpg" alt="" class="splash__image">
            <div class="splash__overlay"></div>
        </section>
        <main class="main">
            <router-link to="/auth" class="back">
                <svg class="back__icon">
                    <use href="@/media/icons/sprites.svg#left" />
                </svg>
            </router-link>
            <div class="main__inner">
                <router-link to="/auth" class="back --inner">
                    <svg class="back__icon">
                        <use href="@/media/icons/sprites.svg#left" />
                    </svg>
                </router-link>
                <h1 v-if="isLog" class="main__title">Авторизация</h1>
                <h1 v-else class="main__title">Регистрация</h1>
                <h2 v-if="isLog" class="main__subtitle">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Harum, repudiandae!</h2>
                <h2 v-else class="main__subtitle">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Harum, repudiandae!</h2>

                <form @submit.prevent="Submit" class="form">
                    <div class="user">
                        <img v-if="userData.user.avatar" :src="userData.user.avatar" alt="" class="user__avatar">
                        <img v-else src="@/media/images/filler.jpg" alt="" class="user__avatar">
                        <div class="user__left">
                            <div class="user__top">
                                <div v-if="isLog" class="user__name">{{ userData.user.first_name }} {{ userData.user.last_name }}</div>
                                <input v-if="!isLog" v-model="name" type="text" class="user__name --input" :class="{ '--wrong' : isWrongName }" @mouseenter="isWrongName = false" placeholder="Соколова Ульяна Владимировна">
                                <!-- <svg class="user__icon"><use href="@/media/icons/sprites.svg#heart" /></svg> -->
                                <img v-if="isStudent && isLog" src="@/media/icons/student.png" alt="" class="user__icon">
                                <img v-else-if="!isStudent && isLog && !isUser" src="@/media/icons/professor.png" alt="" class="user__icon">
                            </div>
                            <div class="user__bottom">
                                <div class="user__username">{{ this.username }}</div>
                                <div v-if="isStudent" class="user__decor">•</div>
                                <div v-if="isStudent" class="user__student-code">{{ userData.student_code }}</div>
                            </div>
                        </div>
                        <!-- <div v-if="!isLog" class="user__right">
                            <label class="type">
                                <div class="type__title">Студент</div>
                                <input type="radio" name="type">
                            </label>
                            <label class="type">
                                <div class="type__title">Доцент</div>
                                <input type="radio" name="type">
                            </label>
                        </div> -->
                    </div>
                    <div class="input">
                        <div class="input__placeholder">
                            Пароль
                            <svg><use href="@/media/icons/sprites.svg#password" /></svg>
                        </div>
                        <input v-model="password" type="password" :class="{ '--wrong' : isWrongPassword }" @mouseenter="isWrongPassword = false" placeholder="**********">
                    </div>
                    <button v-if="isLog" class="form__button">Авторизоваться</button>
                    <button v-else class="form__button">Зарегистрироваться</button>
                </form>
            </div>
        </main>
    </div>
</template>

<script>
import { JWTDecode } from '@/utils/jwt.js'
import { SetCookie } from '@/utils/cookie.js'
import { POST, GET } from '@/utils/fetch.js'


import Loader from '@/components/Loader.vue'



export default {
    name: 'Auth',
    components: {
        Loader
    },
    data() {
        return {
            userData: {
                user: {},
            },

            name: '',
            username: localStorage.getItem('username'),
            password: '',

            loaderActive: false,
            isWrongName: false,
            isWrongPassword: false,

            isLog: localStorage.getItem('type') === 'none' ? false: true,
            isUser: localStorage.getItem('type') === 'user' ? true: false,
            isStudent: localStorage.getItem('type') === 'student' ? true: false,
        }
    },
    mounted() {
        this.GetUser()
    },
    methods: {
        async GetUser() {
            if (localStorage.getItem('type') != 'none') {
                const url = `${localStorage.getItem('type')}/${localStorage.getItem('username')}`

                const response = await GET(url)

                if (response.status === 200) {
                    this.userData = response.data
                }
            }
        },
        async Submit() {
            const url = `token`
            const json = {
                name: this.name.toLowerCase(),
                username: localStorage.getItem('username').toLowerCase(),
                password: this.password,
            }

            if (localStorage.getItem('username') && localStorage.getItem('type') !== 'none') {
                if (this.password) {
                    const response = await POST(url, json)

                    if (response.status === 200) {
                        SetCookie('refresh', response.data.refresh, JWTDecode(response.data.refresh).exp, 'y')
                        SetCookie('access', response.data.access, JWTDecode(response.data.access).exp, 'y')

                        this.$router.push('/rating')
                    } else {
                        this.isWrongPassword = true
                    }
                } else {
                    this.isWrongPassword = true
                }
            } else if (localStorage.getItem('username') && localStorage.getItem('type') === 'none') {
                const url = `create-student`
                
                if (this.name && this.password) {
                    const response = await POST(url, json)

                    if (response.status === 200) {
                        const url = `token`
                        
                        const response = await POST(url, json)

                        if (response.status === 200) {
                            SetCookie('refresh', response.data.refresh, JWTDecode(response.data.refresh).exp, 'y')
                            SetCookie('access', response.data.access, JWTDecode(response.data.access).exp, 'y')

                            this.$router.push('/rating')
                        }
                    } else {
                        if (!this.name) this.isWrongName = true
                        if (!this.password) this.isWrongPassword = true
                    }
                } else {
                    if (!this.name) this.isWrongName = true
                    if (!this.password) this.isWrongPassword = true
                }
            } else {
                this.$router.push('/auth')
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

    position: relative

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

.back
    position: absolute

    top: 5%
    left: 5%


    &.--inner
        display: none

        @include MediaW(768px)
            display: block

    @include MediaW(768px)
        display: none

.back__icon
    width: 24px
    height: 24px

.main__inner
    position: relative

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

.user
    margin-bottom: 32px
    padding: 16px 12px

    display: flex

    align-items: center

    background-color: #fff
    box-shadow: 0 5px 10px rgba(#000, .05)

.user__left,
.user__top,
.user__bottom,
.user__right
    display: flex

.user__left
    width: 100%

    flex-direction: column
    
    row-gap: 4px

.user__top
    width: 100%

    align-items: center

    column-gap: 6px

.user__avatar
    margin-right: 16px

    width: 64px
    height: 64px

    border-radius: 50%

    box-shadow: 0 5px 10px rgba(#000, .1)

    animation: td__avatar 10s ease-in-out infinite


    @include MediaW(1024px)
        width: 56px
        height: 56px

.user__name
    font-size: 14px

    transition: box-shadow .75s ease-in-out


    &.--input
        width: 100%

    &.--wrong
        box-shadow: 0 5px 10px rgba(red, .15)

    
    @include MediaW(1440px)
        font-size: 12.25px

    @include MediaW(1024px)
        font-size: 10.5px

    @include MediaW(768px)
        font-size: 12.25px

    @include MediaW(425px)
        font-size: 10px

.user__icon
    min-width: 16px
    width: 16px
    min-height: 16px
    height: 16px

.user__bottom
    column-gap: 4px

    font-size: 12px
    font-weight: 300


    @include MediaW(1440px)
        font-size: 10px

    @include MediaW(1024px)
        font-size: 9px

    @include MediaW(768px)
        font-size: 10px

    @include MediaW(425px)
        font-size: 9px

.user__username
    font-weight: 400

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
</style>
