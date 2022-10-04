<template>
    <div class="page">
        <!-- <Loader /> -->
        <!-- <Modal /> -->
        <!-- <Pop /> -->

        <Bar :barData="barData" section="events" />
        <Header section="event" sectionName="Мероприятие" />

        
        <div class="wrapper">
            <main class="main">
                <form @submit.prevent="Submit" class="form">
                    <div class="form__top">
                        <label>
                            <img v-if="image !== null" :src="image" alt="" class="form__image">
                            <img v-else src="@/media/images/splash.jpg" alt="" class="form__image">
                            <input type="file" name="file" @change="Upload" class="hide">
                        </label>
                        <div class="group group__3">
                            <div class="select">
                                <div class="select__placeholder">Создатель</div>
                                <select v-model="creatorId">
                                    <option v-for="i in professors" :key="i.id" :value="i.id">
                                        {{ i.user.last_name }} {{ i.user.first_name }} {{ i.user.middle_name }}
                                    </option>
                                </select>
                            </div>
                            <div class="input">
                                <div class="input__placeholder">Название</div>
                                <input v-model="eventName" type="text" placeholder="Name of Event" class="form__input">
                            </div>
                            <div class="select">
                                <div class="select__placeholder">Категория</div>
                                <select v-model="categoryId">
                                    <option v-for="i in categories" :key="i.id" :value="i.id">{{ i.category }}</option>
                                </select>
                            </div>
                        </div>
                        <div class="group group__2">
                            <div class="input">
                                <div class="input__placeholder">Дата начала</div>
                                <input v-model="dateStart" type="text" v-mask="'####-##-## ##:##'" placeholder="2022-04-27 14:14" class="form__input">
                            </div>
                            <div class="input">
                                <div class="input__placeholder">Дата окончания</div>
                                <input v-model="dateEnd" type="text" v-mask="'####-##-## ##:##'" placeholder="2022-04-27 14:14" class="form__input">
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

import { mask } from 'vue-the-mask'


import Loader from '@/components/Loader.vue'
import Modal from '@/components/Modal.vue'
import Pop from '@/components/Pop.vue'

import Bar from '@/components/main/Bar.vue'
import Header from '@/components/main/Header.vue'

import Pagination from '@/components/main/Pagination.vue'



export default {
    name: 'Event',
    components: {
        Loader, Modal, Pop,
        Bar, Header, Pagination,
    },
    directives: { mask },
    data() {
        return {
            barData: {
                user: {},
            },

            image: null,
            creatorId: 0,
            eventName: '',
            categoryId: 0,
            // status: 0,
            dateStart: '',
            dateEnd: '',

            professors: [],
            categories: [],
        }
    },
    created() {
        document.title = 'Мероприятие'
    },
    mounted() {
        this.IsAuth()

        this.GetUser()
        
        this.Professors()
        this.Categories()
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
        async Submit(e) {
            const url = `create-event`
            const json = {
                creator_id: this.creatorId,
                name: this.eventName,
                category_id: this.categoryId,
                // status: this.status,
                date_start: this.dateStart,
                date_end: this.dateEnd,
            }
            
            const response = await POST(url, json, undefined, e.target.file.files[0])


            if (response.status === 200) {
                this.$router.push('/events')
            }
            
        },
        async Professors() {
            const url = `professors`


            const response = await GET(url)


            if (response.status === 200) this.professors = response.data
        },
        async Categories() {
            const url = `categories`


            const response = await GET(url)


            if (response.status === 200) this.categories = response.data
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
        Upload(e) {
            const file = e.target.files[0]
            this.image = URL.createObjectURL(file)
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

.hide
    display: none

.select,
.input
    position: relative

.select__placeholder,
.input__placeholder
    position: absolute

    top: 12px
    left: 12px

    font-size: 12px
    font-weight: 300

select
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
    padding: 40px 16px 16px

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
        grid-template-columns: 1fr 1fr

    &.group__3
        margin-bottom: 16px

        grid-template-columns: 1fr 2fr 1fr
</style>
