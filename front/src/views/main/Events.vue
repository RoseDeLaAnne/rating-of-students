<template>
    <div class="page">
        <Bar :barData="userData" section="events" />
        <Header :ae="events" :headerData="copyData" section="events" sectionName="Мероприятия" @update="UpdateData" />


        <div class="wrapper">
            <main v-if="show == true" class="main">
                <section class="table">
                    <div class="tbody">
                        <div class="trs">
                            <div @click="AddEvent(i.id, 'main')" v-for="i in data" :key="i.id" class="tr" :class="{ '--active' : events.includes(`${i.id}`) }">
                                <div class="td">
                                    <router-link @click="AddEvent(i.id, 'none')" :to="'/event/' + i.id" class="td__inner">
                                        <img v-if="i.image" :src="i.image" alt="" class="td__image">
                                        <img v-else src="@/media/images/filler.jpg" alt="" class="td__image">
                                        <div class="td__value event">{{ i.name }}</div>
                                    </router-link>
                                    <div class="hint"></div>
                                </div>
                                <div class="td">
                                    <router-link @click="AddEvent(i.id, 'none')" :to="'/' + i.creator.user.username" class="td__inner">
                                        <img v-if="i.creator.user.avatar" :src="i.creator.user.avatar" alt="" class="td__avatar">
                                        <img v-else src="@/media/images/filler.jpg" alt="" class="td__avatar">
                                        <div class="td__value">{{ i.creator.user.last_name }} {{ i.creator.user.first_name }}</div>
                                    </router-link>
                                    <div class="hint"></div>
                                </div>
                                <div class="td">
                                    <div class="td__inner">
                                        <svg class="td__icon"><use href="@/media/icons/sprites.svg#role" /></svg>
                                        <div class="td__value category">{{ i.category.category }}</div>
                                    </div>
                                </div>
                                <div class="td">
                                    <div class="td__inner">
                                        <svg class="td__icon"><use href="@/media/icons/sprites.svg#date" /></svg>
                                        <div class="td__value">{{ i.date_start }}</div>
                                    </div>
                                </div>
                                <div class="td">
                                    <div class="td__inner">
                                        <svg class="td__icon"><use href="@/media/icons/sprites.svg#date" /></svg>
                                        <div class="td__value">{{ i.date_end }}</div>
                                    </div>
                                </div>
                                <div class="td">
                                    <div class="td__inner">
                                        <div v-if="i.status === 1" class="td__value status --accept">Активно</div>
                                        <div v-else-if="i.status === -1" class="td__value status --decline">Закончено</div>
                                        <div v-else class="td__value status">Неизвестно</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </main>
            <main v-else-if="show == false" class="main --empty">
                <Empty title="Извините, но мероприятия отсутствуют на сервере" subtitle="Добавьте мероприятия, чтобы увидеть их" />
            </main>


            <Loader :active="loader" />
            <!-- <Pop /> -->

            <Pagination section="events" :data="array" @update="UpdateDataPag" @updateObject="UpdateObject" />
        </div>
    </div>
</template>

<script>
import { JWTDecode } from '@/utils/jwt.js'
import { SetCookie, DeleteCookie, GetCookie } from '@/utils/cookie.js'
import { POST, GET } from '@/utils/fetch.js'


import Loader from '@/components/Loader.vue'
import Modal from '@/components/Modal.vue'
import Pop from '@/components/Pop.vue'

import Bar from '@/components/main/Bar.vue'
import Header from '@/components/main/Header.vue'

import Empty from '@/components/main/Empty.vue'

import Pagination from '@/components/main/Pagination.vue'



export default {
    name: 'Events',
    components: {
        Loader, Modal, Pop,
        Bar, Header, Empty, Pagination,
    },
    data() {
        return {
            userData: {
                user: {},
            },
            data: [],
            copyData: [],
            
            show: null,

            loader: true,

            events: localStorage.getItem('events') ? localStorage.getItem('events').split(',') : [],

            array: {
                count: 0,
                previous: '',
                next: '',
            },

            zone: false,
        }
    },
    computed: {
        unique() {
            return this.events.filter((v, i, a) => a.indexOf(v) === i);
        },
    },
    created() {
        document.title = 'Мероприятия'
    },
    mounted() {
        this.IsAuth()

        this.GetUser()
        this.Data()
    },
    methods: {
        UpdateDataPag(data) {
            this.data = data
        },
        UpdateObject(data) {
            this.array = data
        },
        async IsAuth() {
            if (GetCookie('refresh') && !GetCookie('access')) this.UpdateToken()
            if (!GetCookie('refresh') && !GetCookie('access')) this.$router.push('/auth')
        },
        async UpdateToken() {
            const url = `token/refresh`
            const json = {
                refresh: GetCookie('refresh')
            }

            const response = await POST(url, json)

            if (response.status === 200) {
                SetCookie('access', response.data.access, JWTDecode(response.data.access).exp, 'y')

                this.GetUser()
                this.Data()
            } else this.$router.push('/auth')
        },

        async GetUser() {
            const url = `${JWTDecode(GetCookie('access')).type}/${JWTDecode(GetCookie('access')).username}`

            const response = await GET(url, GetCookie('access'))

            if (response.status === 200) {
                if (JWTDecode(GetCookie('access')).type === 'none') {
                    this.userData.user = response.data
                } else {
                    this.userData = response.data
                }
            }
        },
        async Data() {
            const url = `events`

            const response = await GET(url, GetCookie('access'))

            if (response.status === 200) {
                this.data = response.data.results
                this.copyData = response.data.results

                this.array.count = Math.ceil(response.data.count/7)
                this.array.next = response.data.next
                this.array.previous = response.data.previous

                if (this.data.length) this.show = true
                else this.show = false

                this.loader = false
            }
        },
        UpdateData(data) {
            this.data = data
            this.events = []

            if (this.data.length) this.show = true
            else this.show = false
        },
        AddEvent(id, zone) {
            if (zone === 'none') {
                this.zone = true
            } else {
                if (this.zone === false) {
                    if (this.events.includes(`${id}`)) {
                        this.events.splice(this.events.indexOf(`${id}`), 1)
                    } else {
                        this.events.push(`${id}`)
                    }
                    localStorage.setItem('events', this.unique)
                }
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



.tr
    padding: 16px

    grid-template-columns: 1.5fr 1.125fr 1fr .9375fr .9375fr .5fr

    background-color: #FFF
    box-shadow: 0 5px 10px rgba(#000, .1)
    
    border-radius: 16px

    opacity: .9

    transition: box-shadow .75s ease-in-out, opacity .75s ease-in-out
    
    cursor: pointer


    &.--active,
    &:hover
        opacity: 1

    &.--active
        box-shadow: 0 5px 10px rgba(#000, .5)

    &:hover
        box-shadow: 0 5px 10px rgba(#000, .75)

    
    @include MediaW(1600px)
        grid-template-columns: 1.25fr 0.875fr 0.875fr

        column-gap: 24px
        row-gap: 32px

.td
    display: flex

    @include MediaW(1600px)
        justify-content: center

.td__inner,
.td__value
    display: inline-flex

    align-items: center
    
    column-gap: 10px

.td__value
    &.event
        font-size: 14px
        font-weight: 400
    
    &.category
        padding: 6px 12px

        column-gap: 0

        color: #FFF
        background-color: #000
        box-shadow: 0 5px 10px rgba(#000, .1)

        border-radius: 20px

    &.status
        &:before
            content: ''

            width: var(--tdIconSize)
            height: var(--tdIconSize)

            border-radius: 50%

        &.--accept
            &:before
                background-color: #81b29a

        &.--decline
            &:before
                background-color: #e07a5f

.td__image
    width: var(--tdImageWidth)
    height: var(--tdImageHeight)

    box-shadow: 0 5px 10px rgba(#000, .25)

    border-radius: 16px

    transition: transform .75s ease-in-out, box-shadow .75s ease-in-out


    &:hover
        transform: scale(1.125)

        box-shadow: 0 5px 10px rgba(#000, .5)

.td__avatar
    width: var(--tdAvatarSize)
    height: var(--tdAvatarSize)

    box-shadow: 0 5px 10px rgba(#000, .1)

    border-radius: 50%

    transition: transform .75s ease-in-out, box-shadow .75s ease-in-out, border-radius .75s ease-in-out


    &:hover
        transform: scale(2)

        box-shadow: 0 5px 10px rgba(#000, .2)

        animation: td__avatar 10s ease-in-out infinite

.td__icon
    width: var(--tdIconSize)
    height: var(--tdIconSize)
</style>
