<template>
    <div class="pagination">
        <div @click="Previous" class="pagination__side">
            <svg class="pagination__icon">
                <use href="@/media/icons/sprites.svg#left" />
            </svg>
        </div>
        <div class="pagination__middle">
            <input v-model="currentPage" type="text" class="pagination__current" maxlength="3" placeholder="1">
            <div class="pagination__decor"></div>
            <div class="pagination__count">{{ data.count }}</div>
        </div>
        <div @click="Next" class="pagination__side">
            <svg class="pagination__icon">
                <use href="@/media/icons/sprites.svg#right" />
            </svg>
        </div>
    </div>
</template>

<script>
import { JWTDecode } from '@/utils/jwt.js'
import { SetCookie, DeleteCookie, GetCookie } from '@/utils/cookie.js'
import { POST, GET } from '@/utils/fetch.js'



export default {
    name: 'Pagination',
    props: {
        data: Array,
        section: String,
    },
    data() {
        return {
            currentPage: 1,
        }
    },
    mounted() {},
    methods: {
        async Previous() {
            if (this.data.previous !== null) {
                this.currentPage -= 1
                this.Fetch()
            }
        },
        async Next() {
            if (this.data.next !== null) {
                this.currentPage += 1
                this.Fetch()
            }
        },
        async Fetch() {
            if (this.section === 'applications' && JWTDecode(GetCookie('access')).type === 'professor') var url = `api/applications-professor/${JWTDecode(GetCookie('access')).user_id}/?page=${this.currentPage}`
            else if (this.section === 'applications' && JWTDecode(GetCookie('access')).type === 'student') {
                var url = `api/applications-student/${JWTDecode(GetCookie('access')).user_id}/?page=${this.currentPage}`
            }
            else if (this.section === 'applications' && JWTDecode(GetCookie('access')).type === 'none') var url = `api/applications/?page=${this.currentPage}`
            else if (this.section === 'rating') var url = `api/students/?page=${this.currentPage}`
            else if (this.section === 'events') var url = `api/events/?page=${this.currentPage}`

            const response = await fetch(url)
            const data = await response.json()

            var object = {
                count: Math.ceil(data.count/7),
                previous: data.previous,
                next: data.next,
            }

            this.$emit('update', data.results)
            this.$emit('updateObject', object)
        }
    },
}
</script>

<style lang="sass" scoped>
@import @/styles/keyframes
@import @/styles/mixins
@import @/styles/transitions
@import @/styles/variables



.pagination
    padding: 10px 20px

    position: fixed

    bottom: 20px
    left: calc(50% + var(--barWidth))

    transform: translate(calc(-50% - calc(var(--barWidth)/2)), 0)

    display: flex

    align-items: center

    column-gap: 30px

    background-color: #FFF
    box-shadow: 0 5px 10px rgba(#000, .1)

    border-radius: 16px

    transition: box-shadow .75s ease-in-out


    &:hover
        box-shadow: 0 5px 10px rgba(#000, .25)


        .pagination__decor
            background-color: #888

.pagination__side,
.pagination__icon
    min-width: 22px
    width: 22px
    min-height: 22px
    height: 22px

.pagination__side
    cursor: pointer


    &:hover
        .pagination__icon
            fill: #888

.pagination__icon
    transition: fill .75s ease-in-out

.pagination__middle
    display: flex

    align-items: center

    column-gap: 15px

.pagination__current,
.pagination__count
    width: 40px

    font-weight: 300

    text-align: center

    transition: color .75s ease-in-out


    &:hover
        color: #888

.pagination__current
    font-size: 20px
    font-weight: 400

    cursor: pointer

.pagination__decor
    width: 1px
    height: 50px

    background-color: #444

    border-radius: 16px

    transition: background-color .75s ease-in-out
</style>
