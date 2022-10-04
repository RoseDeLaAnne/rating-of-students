<template>
    <div class="page">
        <Bar :barData="userData" />


        <div class="wrapper">
            <main class="main">
                <div>
                    <div class='theme'>
                        <img src="@/media/images/splash.jpg" alt="" class='theme__img' />
                        <div class='theme__overlay'></div>
                    </div>
                    <div class='user'>
                        <img v-if="data.user.avatar" :src="data.user.avatar" alt="" class='user__avatar' />
                        <img v-else src="@/media/images/filler.jpg" alt="" class='user__avatar' />
                        <div class='info'>
                            <div class="info-section">
                                <div class='name'>
                                    <span class='name__last'>{{ data.user.last_name }}</span> <span class='name__first'>{{ data.user.first_name }}</span> <span class='name__middle'>{{ data.user.middle_name }}</span>
                                </div>
                                <img v-if="isStudent" src="@/media/icons/student.png" alt="" class="category-icon" />
                                <img v-else-if="isProfessor" src="@/media/icons/professor.png" alt="" class="category-icon" />
                                <img v-else src="@/media/icons/admin.png" alt="" class="category-icon" />
                            </div>
                            <div v-if="isStudent && data.speciality" class='info-section'>
                                <div class='department'>
                                    {{ data.speciality.department.name }}
                                </div>
                                <div class="decor">&nbsp;•&nbsp;</div>
                                <div class="speciality">
                                    {{ data.speciality.speciality }}
                                </div>
                                <div class="decor">,&nbsp;</div>
                                <div v-if="data.course" class="course">
                                    {{ data.course }} курс
                                </div>
                                <div v-else class="course">
                                    0 курс
                                </div>
                            </div>
                            <div v-else-if="isProfessor" class="info-section">
                                <div class='department'>
                                    {{ department.name }}
                                </div>
                            </div>
                            <div v-if="isStudent" class='info-section bottom'>
                                <div v-if="data.student_code" class="student-code">
                                    {{ data.student_code }}
                                </div>
                                <div v-else class="student-code">
                                    None
                                </div>
                                <div class="decor">
                                    •
                                </div>
                                <div class="rating-overall">
                                    {{ data.rating }}
                                </div>
                                <svg class='rating-icon'>
                                    <use href="@/media/icons/sprites.svg#rating" />
                                </svg>
                            </div>
                        </div>
                    </div>
                    <div v-if="isStudent" class='rating'>
                        <div class='rating__title'>Рейтинг</div>
                        <div class='rating__i'>
                            <div class="rating__icon_div">
                                <img src="@/media/icons/study.png" alt="" class="rating__icon" />
                                <div class="hint">
                                    Учёба
                                </div>
                            </div>
                            <div class='rating__bar'>
                                <div class='filler' :style="{ width: data.rating_study/50 + '%' }"></div>
                            </div>
                            <div class="rating__count">{{ data.rating_study }}</div>
                        </div>
                        <div class='rating__i'>
                            <div class="rating__icon_div">
                                <img src="@/media/icons/science.png" alt="" class="rating__icon" />
                                <div class="hint">
                                    Наука
                                </div>
                            </div>
                            <div class='rating__bar'>
                                <div class='filler' :style="{ width: data.rating_science/50 + '%' }"></div>
                            </div>
                            <div class="rating__count">{{ data.rating_science }}</div>
                        </div>
                        <div class='rating__i'>
                            <div class="rating__icon_div">
                                <img src="@/media/icons/innovations.png" alt="" class="rating__icon" />
                                <div class="hint">
                                    Инновации
                                </div>
                            </div>
                            <div class='rating__bar'>
                                <div class='filler' :style="{ width: data.rating_innovations/50 + '%' }"></div>
                            </div>
                            <div class="rating__count">{{ data.rating_innovations }}</div>
                        </div>
                        <div class='rating__i'>
                            <div class="rating__icon_div">
                                <img src="@/media/icons/culture.png" alt="" class="rating__icon" />
                                <div class="hint">
                                    Культура
                                </div>
                            </div>
                            <div class='rating__bar'>
                                <div class='filler' :style="{ width: data.rating_culture/50 + '%' }"></div>
                            </div>
                            <div class="rating__count">{{ data.rating_culture }}</div>
                        </div>
                        <div class='rating__i'>
                            <div class="rating__icon_div">
                                <img src="@/media/icons/sport.png" alt="" class="rating__icon" />
                                <div class="hint">
                                    Спорт
                                </div>
                            </div>
                            <div class='rating__bar'>
                                <div class='filler' :style="{ width: data.rating_sport/50 + '%' }"></div>
                            </div>
                            <div class="rating__count">{{ data.rating_sport }}</div>
                        </div>
                        <div class='rating__i'>
                            <div class="rating__icon_div">
                                <img src="@/media/icons/work.png" alt="" class="rating__icon" />
                                <div class="hint">
                                    Работа
                                </div>
                            </div>
                            <div class='rating__bar'>
                                <div class='filler' :style="{ width: data.rating_work/50 + '%' }"></div>
                            </div>
                            <div class="rating__count">{{ data.rating_work }}</div>
                        </div>
                    </div>
                    <div v-if="isStudent" class="achievements">
                        <div class="achievements__title">
                            Достижения
                        </div>
                        <table>
                            <thead>
                                <tr>
                                    <td>
                                        Номер
                                    </td>
                                    <td>
                                        Название
                                    </td>
                                    <td>
                                        Категория
                                    </td>
                                    <td>
                                        Роль
                                    </td>
                                    <td>
                                        Дата
                                    </td>
                                    <td>
                                        Баллы
                                    </td>
                                </tr>
                            </thead>
                            <tbody v-if="achievements.length">
                                <tr v-for="i in achievements" :key="i.id">
                                    <th>
                                        {{ i.id }}
                                    </th>
                                    <th class='event'>
                                        <span class="event_span">
                                            <!-- <router-link to="/" class="event_link">
                                                <img v-if="i.event.image" :src="i.event.image" alt="" class="event__img" />
                                                <img v-else src="@/media/images/filler.jpg" alt="" class="event__img">
                                                <div class="event__name">{{ i.event.name }}</div>
                                            </router-link> -->
                                            <div class="event_link">
                                                <img v-if="i.event.image" :src="i.event.image" alt="" class="event__img" />
                                                <img v-else src="@/media/images/filler.jpg" alt="" class="event__img">
                                                <div class="event__name">{{ i.event.name }}</div>
                                            </div>
                                        </span>
                                    </th>
                                    <th>
                                        {{ i.event.category.category }}
                                    </th>
                                    <th>
                                        {{ i.role.role }}
                                    </th>
                                    <th>
                                        {{ i.date_sended }}
                                    </th>
                                    <th>
                                        {{ i.role.points }}
                                    </th>
                                </tr>
                            </tbody>
                            <tbody v-else>
                                <tr>
                                    <td colspan="6" class="no-data">
                                        Достижения отсутствуют
                                    </td>
                                </tr>
                            </tbody>
                        </table>
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
            userData: {
                user: {},
                department: {},
                speciality: {},
            },

            data: {
                user: {},
                speciality: {
                    department: {},
                },
            },
            achievements: [],
            department: {},

            isStudent: JWTDecode(GetCookie('access')).type === 'student' ? true : false,
            isProfessor: JWTDecode(GetCookie('access')).type === 'professor' ? true : false,
        }
    },
    mounted() {
        this.IsAuth()

        this.GetUser()
        this.Data()
        this.Achievements()
        this.Department()
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
                if (JWTDecode(GetCookie('access')).type === 'student') this.Data()
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
            const url = `student/${this.$route.params.username}`

            const response = await GET(url, GetCookie('access'))

            if (response.status === 200) {
                this.data = response.data
                this.isStudent = true
                this.isProfessor = false
            }
            else if (response.status === 404) {
                const url = `professor/${this.$route.params.username}`

                const response = await GET(url, GetCookie('access'))

                if (response.status === 200) {
                    this.data = response.data
                    this.isStudent = false
                    this.isProfessor = true
                }
            }
        },
        async Achievements() {
            const url = `achievements/${this.$route.params.username}`

            const response = await GET(url, GetCookie('access'))

            if (response.status === 200) this.achievements = response.data
        },
        async Department() {
            const url = `department/${this.$route.params.username}`

            const response = await GET(url, GetCookie('access'))

            if (response.status === 200) this.department = response.data
        }
    },
}
</script>

<style lang="sass" scoped>




.wrapper
    padding-top: 0

.theme
    position: relative

.theme__img,
.theme__overlay
    border-radius: 16px

.theme__img
    width: 100%
    // height: 288px
    height: 256px

.theme__overlay
    position: absolute

    top: 0
    left: 0

    width: 100%
    height: 100%

    background-color: rgba(black, .32)
    box-shadow: 0 4px 12px rgba(black, .08)

.user
    margin-top: -64px
    margin-left: 64px
    margin-bottom: 80px

    position: relative

    display: flex

    align-items: center

    column-gap: 32px

.user__avatar
    width: 224px
    height: 224px

    border-radius: 50%

.info
    margin-top: 32px

    display: flex
    flex-direction: column

.name
    margin-bottom: 8px

    font-size: 24px
    font-weight: 700

.category-icon
    margin-left: 16px
    margin-bottom: 16px

    min-width: 32px
    width: 32px
    height: 32px

.info-section
    display: flex

    align-items: center


    &.bottom
        column-gap: 8px

.rating-icon
    min-width: 14px
    width: 14px
    height: 14px

.rating,
.achievements
    margin-bottom: 24px
    padding: 16px 32px

    box-shadow: 0 4px 12px rgba(black, .1)

    border-radius: 16px

.rating
    display: flex
    flex-direction: column

    row-gap: 12px

.achievements
    margin-bottom: 0
    padding: 16px 32px 24px

.rating__title,
.achievements__title
    margin-bottom: 20px

    font-size: 20px
    font-weight: 700

.rating__i
    display: flex

    align-items: center

    column-gap: 32px

.rating__icon_div
    position: relative

    cursor: pointer


    &:hover
        .hint
            visibility: visible

            opacity: 1

.hint
    padding: 8px 16px

    position: absolute

    top: -32px
    left: 32px

    display: flex

    align-items: center
    justify-content: center

    font-size: 12px
    font-weight: 700

    background-color: white
    box-shadow: 0 5px 10px rgba(black, .1)

    border-radius: 16px

    visibility: hidden

    opacity: 0

    transition: visibility .5s ease-in-out, opacity .5s ease-in-out

    cursor: pointer

.rating__icon
    width: 32px
    height: 32px

.rating__bar
    position: relative

    width: 100%
    height: 10px

    background-color: rgba(black, .1)

    border-radius: 16px

.filler
    position: absolute

    top: 0
    left: 0

    // width: 10%
    width: 0%
    height: 100%

    background-color: #333

    border-radius: 16px

    transition: width 2s ease-in-out

.rating__count
    width: 50px
    
    font-weight: 700

.event
    display: flex

    align-items: center
    justify-content: center

.event_span
    display: inline-block

.event_link
    display: flex

    align-items: center
    justify-content: center

    column-gap: 12px

.event__img
    width: 64px
    height: 32px

    border-radius: 6px

th
    padding: 32px 32px 0px

table
    width: 100%

    text-align: center

.no-data
    padding: 16px 0 6px
    font-size: 14px
    font-weight: 500    
</style>
