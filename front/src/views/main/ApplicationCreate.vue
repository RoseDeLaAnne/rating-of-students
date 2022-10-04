<template>
    <div class="page">
        <!-- <Loader /> -->
        <!-- <Modal /> -->
        <!-- <Pop /> -->

        <Bar :barData="barData" section="applications" />
        <Header section="application" sectionName="Заявка" />

        
        <div class="wrapper">
            <main class="main">
                <form @submit.prevent="Submit" class="form">
                    <div class="form__top">
                        <div class="select">
                            <div class="select__placeholder">Мероприятия</div>
                            <select v-model="eventId" class="one-option">
                                <option v-for="i in events" :key="i.id" :value="i.id">{{ i.name }}</option>
                            </select>
                        </div>
                        <div v-if="!isStudent" class="group group__2">
                            <div class="select">
                                <div class="select__placeholder">Отправитель</div>
                                <select v-if="!isAdmin" v-model="senderId">
                                    <option :value="barData.user.id">{{ barData.user.last_name }} {{ barData.user.first_name }}</option>
                                </select>
                                <select v-else v-model="senderId">
                                    <option v-for="i in senders" :key="i.id" :value="i.id">{{ i.last_name }} {{ i.first_name }}</option>
                                </select>
                            </div>
                            <div class="select">
                                <div class="select__placeholder">Получатель</div>
                                <select v-model="recipientId">
                                    <option v-for="i in recipients" :key="i.user.id" :value="i.id">{{ i.user.last_name }} {{ i.user.first_name }}</option>
                                </select>
                            </div>
                        </div>
                        <div v-if="isStudent" class="select">
                            <div class="select__placeholder">Роль</div>
                            <select v-model="roleId">
                                <option v-for="i in roles" :key="i.id" :value="i.id">{{ i.role }}</option>
                            </select>
                        </div>
                        <div class="group group__2">
                            <div v-if="!isStudent" class="select">
                                <div class="select__placeholder">Роль</div>
                                <select v-model="roleId">
                                    <option v-for="i in roles" :key="i.id" :value="i.id">{{ i.role }}</option>
                                </select>
                            </div>
                            <div v-if="!(isStudent || isProfessor)" class="select">
                                <div class="select__placeholder">Статус</div>
                                <select v-model="status">
                                    <option :value="-1">Отклонена</option>
                                    <option :value="0">В ожидании</option>
                                    <option :value="1">Одобрена</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <button class="form__button">Создать</button>
                </form>
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

            eventId: 0,
            senderId: 0,
            recipientId: 0,
            roleId: 0,
            status: 0,

            events: [],
            senders: [],
            recipients: [],
            roles: [],

            isAdmin: JWTDecode(GetCookie('access')).type === 'none' ? true : false,

            isStudent: JWTDecode(GetCookie('access')).type === 'student' ? true : false,
            isProfessor: JWTDecode(GetCookie('access')).type === 'professor' ? true : false,
        }
    },
    created() {
        document.title = 'Заявка'
    },
    mounted() {
        this.BarData()
        
        this.Events()
        this.Senders()
        this.Recipients()
        this.Roles()
    },
    methods: {
        async BarData() {
            if (!GetCookie('access')) this.UpdateToken()
            if (!localStorage.getItem('username') || localStorage.getItem('username') !== JWTDecode(GetCookie('refresh')).username || localStorage.getItem('username') !== JWTDecode(GetCookie('access')).username) {
                if (GetCookie('refresh')) {
                    localStorage.setItem('username', JWTDecode(GetCookie('refresh')).username)
                } else if (GetCookie('access')) {
                    localStorage.setItem('username', JWTDecode(GetCookie('access')).username)
                } else {
                    this.$router.push('/auth')
                }
            }
            if (!localStorage.getItem('user')) {
                try {
                    const url = `check-student/${localStorage.getItem('username')}`


                    const response = await GET(url, GetCookie('access'))


                    if (response.status === 200) {
                        localStorage.setItem('user', 'student')
                    } else if (response.status === 404) {
                        const url = `check-professor/${localStorage.getItem('username')}`


                        const response = await GET(url, GetCookie('access'))


                        if (response.status == 200) {
                            localStorage.setItem('user', 'professor')
                        } else if (response.status === 404) {
                            // this.$router.push('/auth')
                        }
                    }
                } catch (error) {}
            }


            const url = `${localStorage.getItem('user')}/${localStorage.getItem('username')}`


            try {
                const response = await GET(url, GetCookie('access'))


                if (response.status === 200) {
                    this.barData = response.data
                } else if (response.status === 401) {
                    this.UpdateToken()
                } 
                
                // else {
                //     DeleteCookie('refresh')
                //     DeleteCookie('access')


                //     this.$router.push('/auth')
                // }
            } catch (error) {}
        },
        async Submit() {
            const url = `create-application`
            if (this.isStudent) {
                var json = {
                    event_id: this.eventId,
                    // sender_id: this.recipientId,
                    // recipient_id: this.recipientId,
                    role_id: this.roleId,
                    status: 0,
                }
            } else {
                var json = {
                    event_id: this.eventId,
                    sender_id: this.senderId,
                    recipient_id: this.recipientId,
                    role_id: this.roleId,
                    status: this.status,
                }
            }

            
            const response = await POST(url, json, GetCookie('access'))


            if (response.status === 200) {
                this.$router.push('/applications')
            }
            
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
    },
}
</script>

<style lang="sass" scoped>
@import @/styles/keyframes
@import @/styles/mixins
@import @/styles/transitions
@import @/styles/variables



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
    position: relative

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
    background-color: #222

    transition: background-color .5s ease-in-out


    &:hover
        background-color: rgba(#222, .9)

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
