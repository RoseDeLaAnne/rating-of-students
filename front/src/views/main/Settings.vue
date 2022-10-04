<template>
    <div class="page">
        <!-- <Loader /> -->
        <!-- <Modal /> -->
        <!-- <Pop /> -->

        <Bar :barData="dataU" section="settings" />
        <Header :headerData="dataU" section="settings" sectionName="Настройки" />

        
        <div class="wrapper">
            <main class="main">
                <form @submit.prevent="SaveAvatar">
                    <label class="label">
                        <img v-if="copyDataU.user.avatar !== null" :src="copyDataU.user.avatar" alt="" class="avatar">
                        <img v-else src="@/media/images/filler.jpg" alt="" class="avatar">
                        <input type="file" name="file" @change="Preview" class="hide">
                    </label>
                    <button>Save</button>
                </form>

                <form @submit.prevent="SaveStudentData">
                    <input v-model="dataU.student_code" type="text" placeholder="student-code">
                    <select v-model="dataU.speciality.id" name="speciality">
                        <option v-for="i in specialities" :key="i.id" :value="i.id">{{ i.speciality }}</option>
                    </select>
                    <select v-model="dataU.course" name="course">
                        <option :value="1">1</option>
                        <option :value="2">2</option>
                        <option :value="3">3</option>
                        <option :value="4">4</option>
                    </select>
                    <button>Save</button>
                </form>

                <form @submit.prevent="SaveUserData">
                    <input v-model="dataU.user.username" type="text" placeholder="username">
                    <input v-model="password" type="password" placeholder="password">
                    <input v-model="dataU.user.last_name" type="text" placeholder="фамилия">
                    <input v-model="dataU.user.first_name" type="text" placeholder="имя">
                    <input v-model="dataU.user.middle_name" type="text" placeholder="отчество">
                    <input v-model="dataU.user.email" type="text" placeholder="email">
                    <input v-model="dataU.user.phone_number" type="text" placeholder="phone-number">
                    <button>Save</button>
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
    name: 'Settings',
    components: {
        Loader, Modal, Pop,
        Bar, Header, Pagination,
    },
    data() {
        return {
            dataU: {
                user: {},
                speciality: {},
            },
            copyDataU: {
                user: {},
                speciality: {},
            },
            specialities: [],
            studentData: {
                studentCode: null,
                specialityId: 1,
                course: 1,
            },
            password: null,
        }
    },
    created() {
        document.title = 'Настройки'
    },
    mounted() {
        this.DataU()
        this.Data()
    },
    methods: {
        async DataU() {
            const url = `${JWTDecode(GetCookie('access')).type}/${JWTDecode(GetCookie('access')).username}`

            const response = await GET(url, GetCookie('access'))

            if (response.status === 200) {
                this.dataU = response.data
                this.copyDataU = response.data
            }
        },
        async Data() {
            const url = `specialities`

            const response = await GET(url, GetCookie('access'))

            if (response.status === 200) {
                this.specialities = response.data
            }
        },
        Preview(e) {
            const file = e.target.files[0]
            this.copyDataU.user.avatar = URL.createObjectURL(file)
        },
        async SaveAvatar(e) {
            const url = `save-avatar`
            const json = {
                username: JWTDecode(GetCookie('access')).username,
            }

            const response = await POST(url, json, GetCookie('access'), e.target.file.files[0])
        },
        async SaveStudentData() {
            const url = `save-student-data`
            const json = {
                username: JWTDecode(GetCookie('access')).username,
                student_code: this.dataU.student_code,
                speciality_id: this.dataU.speciality.id,
                course: this.dataU.course,
            }

            const response = await POST(url, json, GetCookie('access'))
        },
        async SaveUserData() {
            const url = `save-user-data`
            const json = {
                username: JWTDecode(GetCookie('access')).username,
                usernameC: this.dataU.user.username,
                last_name: this.dataU.user.last_name,
                first_name: this.dataU.user.first_name,
                middle_name: this.dataU.user.middle_name,
                email: this.dataU.user.email,
                phone_number: this.dataU.user.phone_number,
            }

            const response = await POST(url, json, GetCookie('access'))
        },
    },
}
</script>

<style lang="sass" scoped>
@import @/styles/keyframes
@import @/styles/mixins
@import @/styles/transitions
@import @/styles/variables



.label,
.avatar
    width: 256px
    height: 256px

    border-radius: 50%

.hide
    display: none

button
    padding: 8px 16px

    color: white
    background-color: black
</style>
