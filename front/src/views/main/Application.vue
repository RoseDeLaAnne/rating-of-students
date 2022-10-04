<template>
    <div class="page">
        <!-- <Loader /> -->
        <!-- <Modal /> -->
        <!-- <Pop /> -->

        <Bar :barData="barData" section="applications" />
        <Header :headerData="data" section="application" sectionName="Заявка" />

        
        <div class="wrapper">
            <main class="main">
                <form @submit.prevent="Submit" class="form">
                    <div class="form__top">
                        <div class="select">
                            <div class="select__placeholder">Мероприятие</div>
                            <select v-model="data.eventId">
                                <option v-for="i in events" :key="i.id" :value="i.id">{{ i.name }}</option>
                            </select>
                        </div>
                        <div class="select">
                            <div class="select__placeholder">Отправитель</div>
                            <select v-if="isAdmin" v-model="data.senderId">
                                <option v-for="i in senders" :key="i.id" :value="i.id">{{ i.last_name }} {{ i.first_name }}</option>
                            </select>
                            <select v-if="isProfessor" v-model="data.senderId">
                                <option :value="barData.id">{{ barData.user.last_name }} {{ barData.user.first_name }}</option>
                            </select>
                        </div>
                        <div class="select">
                            <div class="select__placeholder">Получатель</div>
                            <select v-if="isProfessor || isAdmin" v-model="data.recipientId">
                                <option v-for="i in recipients" :key="i.user.id" :value="i.id">{{ i.user.last_name }} {{ i.user.first_name }}</option>
                            </select>
                        </div>
                        <div class="select">
                            <div class="select__placeholder">Роль</div>
                            <select v-model="data.roleId">
                                <option v-for="i in roles" :key="i.id" :value="i.id">{{ i.role }}</option>
                            </select>
                        </div>
                        <div v-if="isAdmin" class="select">
                            <div class="select__placeholder">Статус</div>
                            <select v-if="!isStudent" v-model="data.status">
                                <option :value="-1">Отклонена</option>
                                <option :value="0">В ожидании</option>
                                <option :value="1">Одобрена</option>
                            </select>
                        </div>
                    </div>
                    <button class="form__button" :class="{ '--active' : data.status === 0 || isAdmin }">Изменить</button>
                </form>
                <!-- <div @click="Check">check</div> -->
            </main>


            <!-- <Loader /> -->
            <!-- <Pop /> -->

            <!-- <Pagination /> -->
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

import Pagination from '@/components/main/Pagination.vue'



export default {
    name: 'Application',
    components: {
        Loader, Modal, Pop,
        Bar, Header, Pagination,
    },
    data() {
        return {
            barData: {
                user: {},
            },

            data: {
                image: null,
                eventId: 0,
                senderId: 0,
                recipientId: 0,
                roleId: 0,
                status: 0,
            },

            events: [],
            senders: [],
            recipients: [],
            roles: [],

            isStudent: JWTDecode(GetCookie('access')).type === 'student' ? true : false,
            isProfessor: JWTDecode(GetCookie('access')).type === 'professor' ? true : false,
            isAdmin: JWTDecode(GetCookie('access')).is_superuser === true ? true : false,
        }
    },
    created() {
        document.title = 'Заявка'
    },
    mounted() {
        this.IsAuth()
        this.GetUser()

        this.Data()

        this.Events()
        this.Senders()
        this.Recipients()
        this.Roles()
    },
    methods: {
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
                    this.barData.user = response.data
                } else {
                    this.barData = response.data
                }
            }
        },
        async Data() {
            const url = `application/${this.$route.params.id}`


            try {
                const response = await GET(url, GetCookie('access'))


                if (response.status === 200) {
                    this.data.image = response.data.event.image
                    this.data.eventId = response.data.event.id
                    this.data.senderId = response.data.sender.id
                    this.data.recipientId = response.data.recipient.id
                    this.data.roleId = response.data.role.id
                    this.data.status = response.data.status
                }
            } catch (error) {}
        },
        async Events() {
            const url = `active-events`


            const response = await GET(url, GetCookie('access'))


            if (response.status === 200) this.events = response.data
        },
        async Senders() {
            const url = `senders`


            const response = await GET(url, GetCookie('access'))


            if (response.status === 200) this.senders = response.data
        },
        async Recipients() {
            const url = `recipients`


            const response = await GET(url, GetCookie('access'))


            if (response.status === 200) this.recipients = response.data
        },
        async Roles() {
            const url = `roles`


            const response = await GET(url, GetCookie('access'))


            if (response.status === 200) this.roles = response.data
        },
        async Submit() {
            const url = `application/edit/${this.$route.params.id}`
            if (this.isStudent) {
                var json = {
                    event_id: this.data.eventId,
                    role_id: this.data.roleId,
                }
            } else {
                var json = {
                    event_id: this.data.eventId,
                    sender_id: this.data.senderId, 
                    recipient_id: this.data.recipientId,
                    role_id: this.data.roleId,
                    status: this.data.status,
                }
            }

            if (this.data.status === 0 || this.isAdmin) {
                const response = await POST(url, json, GetCookie('access'))

                if (response.status === 200) {
                    this.$router.push('/applications')
                }
            }
        },
        async UpdateToken() {
            const url = `token/refresh`
            const json = {
                refresh: GetCookie('refresh')
            }


            try {
                const response = await POST(url, json)


                if (response.status === 200) {
                    SetCookie('access', response.data.access, JWTDecode(response.data.access).exp, 'y')
                    

                    this.BarData()
                    this.Data()
                } else {
                    this.$router.push('/auth')
                }
            } catch (error) {}
        },
        Check() {
            console.log(this.data)
        },
    },
}
</script>

<style lang="sass" scoped>
@import @/styles/keyframes
@import @/styles/mixins
@import @/styles/transitions
@import @/styles/variables



.image
    width: 256px
    height: 128px

.form
    padding-bottom: 32px

    height: calc(100vh - var(--headerHeight) - var(--mainPadding)*2)

    display: flex
    flex-direction: column

    justify-content: space-between

.form__image
    margin-bottom: 32px

    width: 100%
    height: 512px

.one-option
    margin-bottom: 16px

.hide
    display: none

.select
    margin-bottom: 24px

    position: relative


    &:last-of-type
        margin-bottom: 0px

.select__placeholder
    position: absolute

    top: 12px
    left: 12px

    font-size: 12px
    font-weight: 300

select
    // padding: 16px
    padding: 40px 16px 16px

    width: 100%

    -webkit-appearance: none
    -moz-appearance: none
    text-indent: 1px
    text-overflow: ''

    background: none
    background-color: white

    border: none

    outline: none

    font-family: Jost, sans-serif
    
    text-align: center

    text-transform: uppercase

    letter-spacing: .2em

    box-shadow: 0 5px 10px rgba(#000, .1)

option
    font-family: Jost, sans-serif
    font-size: 16px

    text-transform: uppercase

    background: none

    border: none

    outline: none

.form__input
    padding: 12px

    width: 100%

    text-align: center

    background-color: white
    box-shadow: 0 5px 10px rgba(#000, .1)

.form__button
    padding: 24px 0

    width: 100%

    font-size: 14px
    font-weight: 600

    letter-spacing: .6em

    color: white
    background-color: rgba(#222, .5)

    transition: background-color .5s ease-in-out


    &.--active
        background-color: #222


        &:hover
            background-color: rgba(#222, .5)


    &:hover
        background-color: rgba(#222, 1)

.group
    display: grid

    align-items: center

    column-gap: 24px


    &.group__2
        margin-bottom: 16px

        grid-template-columns: 1fr 1fr


        &:last-of-type
            margin-bottom: 0px

    &.group__3
        grid-template-columns: 1fr 2fr 1fr
</style>
