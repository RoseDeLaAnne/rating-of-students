<template>
    <div class="page">
        <!-- <Loader /> -->
        <!-- <Modal /> -->
        <!-- <Pop /> -->

        <Bar :barData="userData" section="rating" />
        <Header :headerData="copyData" section="rating" sectionName="Рейтинг" @update="UpdateData" />

        
        <div class="wrapper">
            <main v-if="show == true" class="main">
                <section class="list">
                    <div v-for="i in data" :key="i.id" class="list__i">
                        <router-link :to="'/' + i.user.username" class="list__avatar_link">
                            <img v-if="i.user.avatar" :src="i.user.avatar" alt="" class="list__avatar">
                            <img v-else src="@/media/images/filler.jpg" alt="" class="list__avatar">
                        </router-link>
                        <section class="list__right">
                            <section class="list__top">
                                <div class="list__value">{{ i.speciality.speciality }}</div>
                                <div class="list__value">{{ i.course }} <span>курс</span></div>
                            </section>
                            <section class="list__bottom">
                                <router-link :to="'/' + i.user.username" class="list__subvalue_link">
                                    <div class="list__subvalue"><span>{{ i.user.last_name }}</span> <span>{{ i.user.first_name }}</span> <span>{{ i.user.middle_name }}</span></div>
                                </router-link>
                                <div class="list__subvalue">
                                    <div>{{ i.rating }}</div>
                                    <svg class="list__icon"><use href="@/media/icons/sprites.svg#rating" /></svg>
                                </div>
                            </section>
                        </section>
                    </div>
                </section>
            </main>
            <main v-else-if="show == false" class="main --empty">
                <Empty title="Извините, но студентов с такими данными нет" subtitle="Попробуйте ввести другое значение в поисковую строку" />
            </main>


            <Loader :active="loader" />
            <!-- <Pop /> -->

            <Pagination section="rating" :data="array" @update="UpdateDataPag" @updateObject="UpdateObject" />
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
    name: 'Rating',
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

            array: {
                count: 0,
                previous: '',
                next: '',
            },
        }
    },
    created() {
        document.title = 'Рейтинг'
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
            const url = `students`

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
        },
    },
}
</script>

<style lang="sass" scoped>
@import @/styles/keyframes
@import @/styles/mixins
@import @/styles/transitions
@import @/styles/variables



.list__i
    padding: 10px 16px
    max-width: 640px
    
    flex: 1 1 640px
    
    column-gap: 16px


    @include MediaW(1440px)
        padding: 24px

        max-width: 384px

.list__avatar_link,
.list__avatar
    width: 96px
    height: 96px

    border-radius: 50%


    @include MediaW(1440px)
        width: 160px
        height: 160px

.list__avatar
    box-shadow: 0 5px 10px rgba(#000, .1)

    transition: transform .75s ease-in-out, box-shadow .75s ease-in-out


    &:hover
        transform: scale(1.5)

        box-shadow: 0 5px 10px rgba(#000, .5)

        animation: td__avatar 10s ease-in-out infinite

.list__top,
.list__bottom
    display: flex

    justify-content: space-between


    @include MediaW(1440px)
        flex-direction: column

.list__right
    width: 100%

    display: flex
    flex-direction: column

    row-gap: 10px


    @include MediaW(1440px)
        align-items: center

        row-gap: 20px

.list__value
    font-size: 12px
    font-weight: 300

    text-align: center


    span
        font-size: 10px

.list__subvalue
    display: flex

    align-items: center

    column-gap: 10px

    transition: color .75s ease-in-out


    &:hover
        color: #888

    
    @include MediaW(1440px)
        justify-content: center

.list__icon
    width: 12px
    height: 12px
</style>
