<template>
    <div class="page">
        <Bar :barData="barData" />


        <div class="wrapper">
            <main class="main">
                <div class="top-box">
                    <img class="theme" src="@/media/images/splash.jpg" alt="">
                    <img class="avatar" src="@/media/images/avatar.png" alt="">
                </div>
                
                <div class="middle-box">
                    <h3 class="university">
                        <span class="department">{{ barData.department.name }}</span> <span class="university__decor">/</span> <span class="speciality">{{ barData.speciality.speciality }}</span> <span class="university__decor">, </span> <span class="course">{{ barData.course }} <span>курс</span></span>
                    </h3>
                    <h1 class="name">
                        <span class="name__last">{{ barData.user.last_name }}</span> <span class="name__first">{{ barData.user.first_name }}</span> <span class="name__middle">{{ barData.user.middle_name }}</span>
                    </h1>
                    <h2 class="rating">
                        <span class="rating__value">{{ barData.rating }} <span>балла</span></span>
                    </h2>

                    <div class="ratings">
                        <div class="ratings__i">
                            <div class="ratings__name">Учёба</div>
                            <div class="ratings__decor"></div>
                            <div class="ratings__value">{{ barData.rating_study }}</div>
                        </div>
                        <div class="ratings__i">
                            <div class="ratings__name">Наука</div>
                            <div class="ratings__decor"></div>
                            <div class="ratings__value">{{ barData.science }}</div>
                        </div>
                        <div class="ratings__i">
                            <div class="ratings__name">Инновации</div>
                            <div class="ratings__decor"></div>
                            <div class="ratings__value">{{ barData.rating__innovations }}</div>
                        </div>
                        <div class="ratings__i">
                            <div class="ratings__name">Культура</div>
                            <div class="ratings__decor"></div>
                            <div class="ratings__value">{{ barData.rating__culture }}</div>
                        </div>
                        <div class="ratings__i">
                            <div class="ratings__name">Спорт</div>
                            <div class="ratings__decor"></div>
                            <div class="ratings__value">109</div>
                        </div>
                        <div class="ratings__i">
                            <div class="ratings__name">Работа</div>
                            <div class="ratings__decor"></div>
                            <div class="ratings__value">102</div>
                        </div>
                    </div>

                    <div class="achievements">
                        <div class="achievements__group">
                            <div class="achievements__title">Учёба</div>
                            <div class="achievements__i">
                                <section class="achievements__left">
                                    <div class="achievements__name">День студента</div>
                                </section>
                                <section class="achievements__right">
                                    <div><span class="achievements__role">Выступающий</span> <span class="achievements__decor">, +</span> <span class="achievements__points">100</span></div>
                                    <div class="achievements__date">06-05-2022 | 19:22</div>
                                </section>
                            </div>
                            <div class="achievements__i">
                                <section class="achievements__left">
                                    <div class="achievements__name">День студента</div>
                                </section>
                                <section class="achievements__right">
                                    <div><span class="achievements__role">Выступающий</span> <span class="achievements__decor">, +</span> <span class="achievements__points">100</span></div>
                                    <div class="achievements__date">06-05-2022 | 19:22</div>
                                </section>
                            </div>
                        </div>
                        <div class="achievements__group">
                            <div class="achievements__title">Наука</div>
                            <div class="achievements__i">
                                <section class="achievements__left">
                                    <div class="achievements__name">День студента</div>
                                </section>
                                <section class="achievements__right">
                                    <div><span class="achievements__role">Выступающий</span> <span class="achievements__decor">, +</span> <span class="achievements__points">100</span></div>
                                    <div class="achievements__date">06-05-2022 | 19:22</div>
                                </section>
                            </div>
                            <div class="achievements__i">
                                <section class="achievements__left">
                                    <div class="achievements__name">День студента</div>
                                </section>
                                <section class="achievements__right">
                                    <div><span class="achievements__role">Выступающий</span> <span class="achievements__decor">, +</span> <span class="achievements__points">100</span></div>
                                    <div class="achievements__date">06-05-2022 | 19:22</div>
                                </section>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>

<script>
import { JWTDecode } from '@/utils/jwt.js'
import { SetCookie, DeleteCookie, GetCookie } from '@/utils/cookie.js'
import { POST, GET } from '@/utils/fetch.js'


import Bar from '@/components/main/Bar.vue'



export default {
    name: 'Profile',
    components: {
        Bar,
    },
    data() {
        return {
            barData: {
                user: {},
                department: {},
                speciality: {},
            },
        }
    },
    mounted() {
        this.Data()
    },
    methods: {
        async Data() {
            if (!GetCookie('access')) this.UpdateToken()


            const url = `student/${JWTDecode(GetCookie('access')).username}`


            try {
                const response = await GET(url, GetCookie('access'))


                if (response.status === 200) {
                    this.barData = response.data
                } else if (response.status === 404) {
                    const url = `professor/${JWTDecode(GetCookie('access')).username}`


                    try {
                        const response = await GET(url, GetCookie('access'))

                        
                        if (response.status === 200) {
                            this.barData = response.data
                        } else if (response.status === 404) {
                            this.$router.push('/auth')
                        }
                    } catch (error) {}
                } else if (response.status === 401) {
                    this.UpdateToken()
                }
            } catch (error) {}
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




.wrapper
    padding-top: 0

.top-box
    display: flex
    flex-direction: column

    align-items: center

.theme
    width: 100%
    height: 256px

.avatar
    margin-top: -96px

    width: 256px
    height: 256px

    border-radius: 50%

.middle-box
    display: flex
    flex-direction: column

    align-items: center

.ratings
    display: flex

.ratings__i
    display: flex
    flex-direction: column

.ratings__decor
    width: 1px
    height: 128px

    background-color: black

.ratings__value
    margin-top: -96px

    min-width: 192px
    width: 192px
    min-height: 192px
    height: 192px

    display: flex
    
    align-items: center
    justify-content: center

    background-color: rgba(#222, .2)

    border-radius: 50%

// .achievements__i
//     display: flex

.achievements__i
    display: grid

    grid-template-columns: 1fr 1fr
</style>
