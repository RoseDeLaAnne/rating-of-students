<template>
    <header class="header">
        <section class="header__left">
            <div class="header__path">{{ sectionName }}</div>
        </section>
        <div class="header-box">
            <section v-if="section === 'rating' || section === 'applications' || section === 'events'" class="header__middle">
                <div class="search">
                    <input v-model="search" @input="Search" type="text" class="search__input" placeholder="Поиск">
                    <svg class="search__icon"><use href="@/media/icons/sprites.svg#search" /></svg>
                </div>
            </section>
            <section class="header__right">
                <div v-if="section === 'applications' || section === 'events'" class="actions">
                    <router-link :to="'/' + section + '/create'" class="actions__i --create">
                        <svg class="actions__icon"><use href="@/media/icons/sprites.svg#add" /></svg>
                    </router-link>
                    <div @click="Action('delete')" class="actions__i --delete">
                        <svg class="actions__icon"><use href="@/media/icons/sprites.svg#delete" /></svg>
                    </div>
                </div>
                <div v-if="section === 'applications' && isSuperUser" class="actions">
                    <div @click="Action('accept')" class="actions__i --accept"></div>
                    <div @click="Action('waiting')" class="actions__i --waiting"></div>
                    <div @click="Action('decline')" class="actions__i --decline"></div>
                </div>
            </section>
        </div>
    </header>
</template>

<script>
import { JWTDecode } from '@/utils/jwt.js'
import { SetCookie, DeleteCookie, GetCookie } from '@/utils/cookie.js'
import { POST, GET } from '@/utils/fetch.js'



export default {
    name: 'Header',
    props: {
        ae: {
            type: Array,
        },
        headerData: {
            type: Array,
        },
        section: {
            type: String,
            require: true,
        },
        sectionName: {
            type: String,
            require: true,
        },
    },
    data() {
        return {
            search: '',
            
            array: this.headerData,

            isStaff: JWTDecode(GetCookie('access')).is_staff ? true : false,
            isSuperUser: JWTDecode(GetCookie('access')).is_superuser ? true : false,
        }
    },
    computed: {
        unique() {
            return this.ae.filter((v, i, a) => a.indexOf(v) === i);
        },
    },
    mounted() {},
    methods: {
        // Search() {
        //     if (this.section === 'rating') {
        //         this.array = this.headerData.filter(i => i.student_code.toString().indexOf(this.search) !== -1 || i.course.toString().indexOf(this.search) !== -1 || i.department.name.toLowerCase().indexOf(this.search.toLowerCase()) !== -1 || i.rating.toString().indexOf(this.search) !== -1 || i.speciality.speciality.toLowerCase().indexOf(this.search.toLowerCase()) !== -1 || i.user.first_name.toLowerCase().indexOf(this.search.toLowerCase()) !== -1 || i.user.last_name.toLowerCase().indexOf(this.search.toLowerCase()) !== -1 || i.user.middle_name.toLowerCase().indexOf(this.search.toLowerCase()) !== -1)
        //     } else if (this.section === 'applications') {
        //         this.array = this.headerData.filter(i => i.event.name.toLowerCase().indexOf(this.search.toLowerCase()) !== -1 || i.sender.first_name.toLowerCase().indexOf(this.search.toLowerCase()) !== -1 || i.sender.last_name.toLowerCase().indexOf(this.search.toLowerCase()) !== -1 || i.sender.middle_name.toLowerCase().indexOf(this.search.toLowerCase()) !== -1 || i.recipient.user.first_name.toLowerCase().indexOf(this.search.toLowerCase()) !== -1 || i.recipient.user.first_name.toLowerCase().indexOf(this.search.toLowerCase()) !== -1 || i.recipient.user.first_name.toLowerCase().indexOf(this.search.toLowerCase()) !== -1 || i.role.role.toLowerCase().indexOf(this.search.toLowerCase()) !== -1 || i.date_sended.indexOf(this.search) !== -1 || i.status.toString().indexOf(this.search) !== -1)
        //     } else if (this.section === 'events') {
        //         this.array = this.headerData.filter(i => i.name.toLowerCase().indexOf(this.search.toLowerCase()) !== -1 || i.creator.user.first_name.toLowerCase().indexOf(this.search.toLowerCase()) !== -1 || i.creator.user.last_name.toLowerCase().indexOf(this.search.toLowerCase()) !== -1 || i.creator.user.middle_name.toLowerCase().indexOf(this.search.toLowerCase()) !== -1 || i.category.category.toLowerCase().indexOf(this.search.toLowerCase()) !== -1 || i.date_start.indexOf(this.search) !== -1 || i.date_end.indexOf(this.search) !== -1)
        //     }
        //     this.$emit('update', this.array)
        //     console.log(this.array)
        // },
        // async Search() {
        //     const url = `students-by-key`
        //     const json = {
        //         key: this.search,
        //     }

        //     const response = await POST(url, json, GetCookie('access'))

        //     if (response.status === 200) {

        //     }
        // },
        async Action(type) {
            const url = `action`

            if (this.section === 'applications') {
                var json = {
                    ids: this.unique,
                    page: 'applications',
                    type: type,
                    userType: JWTDecode(GetCookie('access')).type,
                }
            } else if (this.section === 'events') {
                var json = {
                    ids: this.unique,
                    page: 'events',
                    type: type,
                    userType: JWTDecode(GetCookie('access')).type,
                }
            } else {
                var json = {}
            }

            // for (var i in this.headerData) {
            //     console.log(this.headerData[i].id)
            //     for (var y in this.unique) {
            //         if (`${this.headerData[i].id}` === this.unique[y] && this.headerData[i].status != 1) {
            //             console.log('not status 1')
            //         }
            //     }
            // }

            const response = await POST(url, json, GetCookie('access'))

            if (response.status === 200) {
                this.$emit('update', response.data)


                // if (this.section === 'applications') localStorage.removeItem('applications')
                // else if (this.section === 'events') localStorage.removeItem('events')
                // else {
                //     localStorage.removeItem('applications')
                //     localStorage.removeItem('events')
                // }
                localStorage.removeItem('applications')
                localStorage.removeItem('events')
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



.header
    padding: 36px 36px 6px
    position: fixed

    top: 0
    left: var(--barWidth)

    width: calc(100% - var(--barWidth))
    height: var(--headerHeight)

    display: flex

    @include MediaW(1440px)
        flex-direction: column

    @include MediaW(1024px)
        left: 0

        width: 100%

.header__left,
.header__middle,
.header__right
    display: flex

    align-items: center

.header__left,
.header__right
    // width: 30%
    min-width: 512px

.header__left
    @include MediaW(1440px)
        width: 100%

.header__middle
    width: 100%

    opacity: 0
    visibility: hidden

.header__right
    justify-content: flex-end

    column-gap: 16px

.header__path
    font-size: 32px
    font-weight: 300

    letter-spacing: .4em

.search
    position: relative

    width: 100%

.search__input
    padding: 12px 16px 12px 52px

    width: 100%
    
    background-color: #FFF
    box-shadow: 0 5px 10px rgba(#000, .1)

    border-radius: 32px

    opacity: .75

    transition: box-shadow .75s ease-in-out, opacity .75s ease-in-out


    &:hover,
    &:focus
        box-shadow: 0 5px 10px rgba(#000, .2)

        opacity: 1


        + .search__icon
            opacity: 1

.search__icon
    position: absolute

    top: 50%
    left: 16px

    transform: translate(0, -50%)

    width: 20px
    height: 20px

    opacity: .75

    transition: opacity .75s ease-in-out

.header-box
    width: 100%

    display: flex

.actions
    padding: 6px 16px

    display: flex

    background-color: #FFF
    box-shadow: 0 5px 10px rgba(#000, .1)

    border-radius: 16px

    opacity: .75

    transition: box-shadow .75s ease-in-out, opacity .75s ease-in-out


    &:hover
        box-shadow: 0 5px 10px rgba(#000, .2)

        opacity: 1


        .actions__i
            &.--accept,
            &.--waiting,
            &.--decline
                margin-right: 6px

                &:last-of-type
                    margin-right: 0px

.actions__i
    cursor: pointer

    &.--accept,
    &.--waiting,
    &.--decline
        width: 24px
        height: 24px

        border-radius: 50%

        margin-right: -6px

        transition: margin-right .5s ease-in-out, background-color .75s ease-in-out, box-shadow .75s ease-in-out


        &:last-of-type
            margin-right: 0px

    svg
        transition: fill .5s ease-in-out

    &.--create
        margin-right: 12px

        svg
            fill: rgba(#81b29a, .5)

        &:hover
            svg
                fill: rgba(#81b29a, 1)

    &.--delete
        svg
            fill: rgba(#e07a5f, .5)

        &:hover
            svg
                fill: rgba(#e07a5f, 1)

    &.--accept
        background-color: rgba(#81b29a, 1)
        box-shadow: 0 5px 10px rgba(#81b29a, .25)
        

        &:hover
            background-color: #81b29a
            box-shadow: 0 5px 10px rgba(#81b29a, .5)

    &.--waiting
        background-color: rgba(#f2cc8f, 1)
        box-shadow: 0 5px 10px rgba(#f2cc8f, .25)
        

        &:hover
            background-color: #f2cc8f
            box-shadow: 0 5px 10px rgba(#f2cc8f, .5)

    &.--decline
        background-color: rgba(#e07a5f, 1)
        box-shadow: 0 5px 10px rgba(#e07a5f, .25)
        

        &:hover
            background-color: #e07a5f
            box-shadow: 0 5px 10px rgba(#e07a5f, .5)

.actions__icon
    width: 24px
    height: 24px
</style>
