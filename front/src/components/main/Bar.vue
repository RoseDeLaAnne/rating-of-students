<template>
    <div class="bar">
        <section class="bar__top">
            <Brand />
        </section>

        <section class="bar__middle">
            <div class="navigation">
                <div class="navigation__i">
                    <router-link to="/rating" class="navigation__i_link" :class="{ '--active' : section === 'rating' }">
                        <svg class="navigation__icon"><use href="@/media/icons/sprites.svg#rating" /></svg>
                        <div class="navigation__name">Рейтинг</div>
                    </router-link>
                    <div class="hint">
                        <img src="@/media/icons/rating.gif" alt="" class="hint__image">
                        <div class="hint__title">Рейтинг</div>
                        <div class="hint__subtitle">Lorem ipsum dolor sit amet, consectetur adipisicing.</div>
                    </div>
                </div>
                <div class="navigation__i">
                    <router-link to="/applications" class="navigation__i_link" :class="{ '--active' : section === 'applications' }">
                        <svg class="navigation__icon"><use href="@/media/icons/sprites.svg#applications" /></svg>
                        <div class="navigation__name">Заявки</div>
                    </router-link>
                    <div class="hint">
                        <img src="@/media/icons/applications.gif" alt="" class="hint__image">
                        <div class="hint__title">Заявки</div>
                        <div class="hint__subtitle">Lorem ipsum dolor sit amet consectetur adipisicing.</div>
                    </div>
                </div>
                <div v-if="isStaff || isSuperUser" class="navigation__i">
                    <router-link to="/events" class="navigation__i_link" :class="{ '--active' : section === 'events' }">
                        <svg class="navigation__icon"><use href="@/media/icons/sprites.svg#events" /></svg>
                        <div class="navigation__name">Мероприятия</div>
                    </router-link>
                    <div class="hint">
                        <img src="@/media/icons/events.gif" alt="" class="hint__image">
                        <div class="hint__title">Мероприятия</div>
                        <div class="hint__subtitle">Lorem ipsum dolor sit, amet consectetur adipisicing.</div>
                    </div>
                </div>
            </div>
        </section>

        <section class="bar__bottom">
            <div v-if="!isStaff" class="navigation">
                <div class="navigation__i">
                    <router-link to="/settings" class="navigation__i_link">
                        <svg class="navigation__icon"><use href="@/media/icons/sprites.svg#settings" /></svg>
                        <div class="navigation__name">Настройки</div>
                    </router-link>
                    <div class="hint">
                        <img src="@/media/icons/settings.gif" alt="" class="hint__image">
                        <div class="hint__title">Настройки</div>
                        <div class="hint__subtitle">Lorem ipsum dolor sit, amet consectetur adipisicing.</div>
                    </div>
                </div>
            </div>

            <div class="bar__decor"></div>

            <div class="bar__filler"></div>
            <div class="user">
                <router-link :to="'/' + barData.user.username" class="user__avatar_link">
                    <img v-if="barData.user.avatar" :src="barData.user.avatar" alt="" class="user__avatar">
                    <img v-else src="@/media/images/filler.jpg" alt="" class="user__avatar">
                </router-link>
                <div class="rating">
                    <div class="user__rating">100</div>
                    <svg class="user__icon"><use href="@/media/icons/sprites.svg#rating" /></svg>
                </div>

                <div class="user__information">
                    <router-link :to="'/' + barData.user.username" class="user__title_link">
                        <div class="user__title">{{ barData.user.last_name }} {{ barData.user.first_name }}</div>
                    </router-link>
                    <div v-if="isStudent" class="user__subtitle">
                        <div v-if="barData.student_code" class="user__student-code">{{ barData.student_code }}</div>
                        <div v-else class="user__student-code">None</div>
                        <div class="user__decor">•</div>
                        <div class="user__rating">{{ barData.rating }}</div>
                        <svg class="user__icon"><use href="@/media/icons/sprites.svg#rating" /></svg>
                    </div>
                </div>

                <div @click="Logout" class="user__button">Выход</div>
            </div>
        </section>
    </div>
</template>

<script>
import { JWTDecode } from '@/utils/jwt.js'
import { SetCookie, DeleteCookie, GetCookie } from '@/utils/cookie.js'
import { POST, GET } from '@/utils/fetch.js'


import Brand from '@/components/Brand.vue'



export default {
    name: 'Bar',
    components: {
        Brand,
    },
    props: {
        barData: {
            type: Object,
            require: true,
        },
        section: {
            type: String,
            require: true,
        },
    },
    data() {
        return {
            isStudent: JWTDecode(GetCookie('access')).type === 'student' ? true : false,

            isStaff: JWTDecode(GetCookie('access')).is_staff ? true : false,
            isSuperUser: JWTDecode(GetCookie('access')).is_superuser ? true : false,
        }
    },
    mounted() {},
    methods: {
        Logout() {
            localStorage.clear()

            DeleteCookie('refresh')
            DeleteCookie('access')


            this.$router.push('/auth')
        },
    },
}
</script>

<style lang="sass" scoped>
@import @/styles/keyframes
@import @/styles/mixins
@import @/styles/transitions
@import @/styles/variables



.bar
    padding: 24px 12px 20px

    position: fixed

    top: 0
    left: 0

    // width: 
    height: 100vh

    display: flex
    flex-direction: column

    justify-content: space-between

    background-color: #FFF
    box-shadow: 0 5px 10px rgba(#000, .1)

    z-index: 101


    @include MediaW(1024px)
        padding: 16px

        top: auto
        bottom: 0
        left: 0

        width: 100%
        // height: 64px
        height: auto

        flex-direction: row

        column-gap: 128px

.bar__top,
.bar__middle,
.bar__bottom
    display: flex
    flex-direction: column


    @include MediaW(1024px)
        width: 100%

        flex-direction: row

        justify-content: center

.bar__top
    @include MediaW(1024px)
        display: none

.bar__bottom
    row-gap: 24px

.navigation
    display: flex
    flex-direction: column

    align-items: center

    row-gap: 16px


    @include MediaW(1024px)
        flex-direction: row

        column-gap: 16px

.navigation__i
    position: relative

    display: flex

.navigation__i_link
    padding: 12px

    border-radius: 16px

    transition: background-color .5s ease-in-out, box-shadow .5s ease-in-out


    &.--active,
    &:hover
        background-color: #FFF
    
    &.--active
        box-shadow: 0 5px 10px rgba(#000, .125)

    &:hover
        box-shadow: 0 5px 10px rgba(#000, .1)


        .navigation__icon
            fill: #888

        + .hint
            visibility: visible
            opacity: 1

    
    @include MediaW(1024px)
        &:hover
            + .hint
                visibility: visible
                opacity: 1

.navigation__icon
    width: 24px
    height: 24px 

    transition: fill .75s ease-in-out

.navigation__name
    display: none

.hint
    padding: 24px

    position: absolute

    top: 50%
    right: -340px

    transform: translate(0, -50%)

    width: 308px
    height: 280px

    display: flex
    flex-direction: column

    align-items: center
    justify-content: center

    background-color: #FFF
    box-shadow: 0 5px 10px rgba(#000, .25)

    border-radius: 16px

    visibility: hidden
    opacity: 0

    transition: visibility .5s ease-in-out, opacity .5s ease-in-out


    @include MediaW(1024px)
        top: -310px
        left: 50%

        transform: translate(-50%, 0)

.hint__image
    margin-bottom: 32px

    width: 112px
    height: 112px

.hint__title,
.hint__subtitle
    text-align: center

.hint__title
    margin-bottom: 6px

.hint__subtitle
    font-size: 10px
    font-weight: 300

    color: #888

.bar__decor
    width: 100%
    height: 1px

    background-color: #000


    @include MediaW(1024px)
        display: none

.bar__filler,
.user__avatar,
.user__avatar_link
    min-width: 64px
    width: 64px
    min-height: 64px
    height: 64px
    
    border-radius: 50%


    @include MediaW(1024px)
        min-width: 96px
        width: 96px
        min-height: 96px
        height: 96px

.bar__filler
    @include MediaW(1024px)
        display: none

.rating
    display: none


    @include MediaW(1024)
        margin-top: 6px

        display: flex
        align-items: center

        column-gap: 6px

.user
    padding-right: 24px

    position: fixed

    bottom: 20px
    left: 12px

    max-width: 64px
    min-height: 64px

    display: flex

    align-items: center

    background-color: #FFF
    box-shadow: 0 5px 10px rgba(#000, .125)

    border-radius: 32px

    transition: max-width 1s ease-in-out, box-shadow 1s ease-in-out

    overflow: hidden


    &:hover
        max-width: 640px
        box-shadow: 0 5px 10px rgba(#000, .25)


        .user__information,
        .user__button
            opacity: 1

    
    @include MediaW(1024px)
        padding-right: 0

        bottom: 8px
        left: 50%

        transform: translate(-50%, 0)

        max-width: 96px
        min-height: 96px

        flex-direction: column

        background-color: transparent
        box-shadow: none


        &:hover
            max-width: 96px

            box-shadow: none

.user__information
    margin-left: 16px
    margin-right: 26px

    display: flex
    flex-direction: column

    row-gap: 6px

    opacity: 0

    transition: opacity 1s ease-in-out


    @include MediaW(1024px)
        display: none

.user__title
    white-space: nowrap

    transition: color 1s ease-in-out


    &:hover
        color: #888

.user__subtitle
    display: flex

    align-items: center

    column-gap: 6px

    font-size: 12px
    font-weight: 300

.user__student-code
    color: #888

.user__icon
    width: 12px
    height: 12px

.user__button
    padding: 12px 32px

    font-size: 12px

    color: #FFF
    background-color: #000

    border-radius: 32px

    opacity: 0

    transition: color .5s ease-in-out, box-shadow .5s ease-in-out, opacity 1s ease-in-out

    cursor: pointer


    &:hover
        color: #888
        box-shadow: 0 5px 10px rgba(#000, .25)

    
    @include MediaW(1024px)
        display: none
</style>
