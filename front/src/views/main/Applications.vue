<template>
    <div class="page">
        <Bar :barData="userData" section="applications" />
        <Header :ae="applications" :headerData="copyData" section="applications" sectionName="Заявки" @update="UpdateData" />


        <div class="wrapper">
            <main v-if="show == true" class="main">
                <section class="table">
                    <div class="tbody">
                        <div class="trs">
                            <div @click="AddApplication(i.id, 'main')" v-for="i in data" :key="i.id" class="tr" :class="{ '--active' : applications.includes(`${i.id}`) }">
                                <div class="td">
                                    <router-link @click="AddApplication(i.id, 'none')" :to="'/application/' + i.id" class="td__inner">
                                        <img v-if="i.event.image" :src="i.event.image" alt="" class="td__image">
                                        <img v-else src="@/media/images/filler.jpg" alt="" class="td__image">
                                        <div class="td__value event">{{ i.event.name }}</div>
                                    </router-link>
                                    <div class="hint"></div>
                                </div>
                                <div class="td">
                                    <router-link @click="AddApplication(i.id, 'none')" :to="'/' + i.sender.username" class="td__inner">
                                        <img v-if="i.sender.avatar" :src="i.sender.avatar" alt="" class="td__avatar">
                                        <img v-else src="@/media/images/filler.jpg" alt="" class="td__avatar">
                                        <div class="td__value">{{ i.sender.last_name }} {{ i.sender.first_name }}</div>
                                    </router-link>
                                    <div class="hint"></div>
                                </div>
                                <div class="td">
                                    <router-link @click="AddApplication(i.id, 'none')" :to="'/' + i.recipient.user.username" class="td__inner">
                                        <img v-if="i.recipient.user.avatar" :src="i.recipient.user.avatar" alt="" class="td__avatar">
                                        <img v-else src="@/media/images/filler.jpg" alt="" class="td__avatar">
                                        <div class="td__value">{{ i.recipient.user.last_name }} {{ i.recipient.user.first_name }}</div>
                                    </router-link>
                                    <div class="hint"></div>
                                </div>
                                <div class="td">
                                    <div class="td__inner">
                                        <svg class="td__icon"><use href="@/media/icons/sprites.svg#role" /></svg>
                                        <div class="td__value role">
                                            <div>{{ i.role.role }}</div>
                                            <div>, +</div>
                                            <div>{{ i.role.points }}</div>
                                        </div>
                                    </div>
                                </div>
                                <div class="td">
                                    <div class="td__inner">
                                        <svg class="td__icon"><use href="@/media/icons/sprites.svg#date" /></svg>
                                        <div class="td__value">{{ i.date_sended }}</div>
                                    </div>
                                </div>
                                <div class="td">
                                    <div class="td__inner">
                                        <div v-if="i.status === 1" class="td__value status --accept">Одобрена</div>
                                        <div v-else-if="i.status === 0" class="td__value status --waiting">В ожидании</div>
                                        <div v-else-if="i.status === -1" class="td__value status --decline">Отклонена</div>
                                        <div v-else class="status">Неизвестно</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </main>
            <main v-else-if="show == false" class="main --empty">
                <Empty title="Извините, но заявки отсутствуют на сервере" subtitle="Добавьте заявки, чтобы увидеть их" />
            </main>


            <Loader :active="loader" />
            <!-- <Pop /> -->

            <Pagination section="applications" :data="array" @update="UpdateDataPag" @updateObject="UpdateObject" />
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
    name: 'Applications',
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

            applications: localStorage.getItem('applications') ? localStorage.getItem('applications').split(',') : [],

            isStaff: JWTDecode(GetCookie('access')).is_staff ? true : false,
            isSuperUser: JWTDecode(GetCookie('access')).is_superuser ? true : false,

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
            return this.applications.filter((v, i, a) => a.indexOf(v) === i);
        },
    },
    created() {
        document.title = 'Заявки'
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
            if (this.isSuperUser) {
                var url = `applications`
            } else if (JWTDecode(GetCookie('access')).type === 'professor') {
                var url = `applications-professor/${JWTDecode(GetCookie('access')).user_id}`
            } else {
                var url = `applications-student/${JWTDecode(GetCookie('access')).user_id}`
            }

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
            this.applications = []

            if (this.data.length) this.show = true
            else this.show = false
        },
        AddApplication(id, zone) {
            if (zone === 'none') {
                this.zone = true
            } else {
                if (this.zone === false) {
                    console.log('test')
                    if (this.applications.includes(`${id}`)) {
                        this.applications.splice(this.applications.indexOf(`${id}`), 1)
                    } else {
                        this.applications.push(`${id}`)
                    }
                    localStorage.setItem('applications', this.unique)
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

    grid-template-columns: 1.5fr 1.125fr 1.125fr 1fr .75fr .5fr

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
    @include MediaW(1024px)
        font-size: 10px

    &.event
        font-size: 14px
        font-weight: 400


        @include MediaW(1024px)
            font-size: 12px
    
    &.role
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

        &.--waiting
            &:before
                background-color: #f2cc8f

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
