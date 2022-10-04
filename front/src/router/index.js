import { createRouter, createWebHistory } from 'vue-router'


import { JWTDecode } from '@/utils/jwt.js'
import { GetCookie } from '@/utils/cookie.js'


import Land from '@/views/Land.vue'

import Auth from '@/views/auth/Auth.vue'
import Confirm from '@/views/auth/Confirm.vue'

import Rating from '@/views/main/Rating.vue'

import Applications from '@/views/main/Applications.vue'
import ApplicationCreate from '@/views/main/ApplicationCreate.vue'
import Application from '@/views/main/Application.vue'

import Events from '@/views/main/Events.vue'
import EventCreate from '@/views/main/EventCreate.vue'
import Event from '@/views/main/Event.vue'

import Profile from '@/views/main/Profile.vue'
import Settings from '@/views/main/Settings.vue'



const routes = [
    {
        path: '/',
        name: 'land',
        component: Land,
        redirect: '/auth',
    },
    {
        path: '/auth',
        name: 'auth',
        component: Auth,
        beforeEnter: (to, from, next) => {
            if (GetCookie('access')) next('/rating')
            else next()
        },
    },
    {
        path: '/auth/confirm',
        name: 'confirm',
        component: Confirm,
        beforeEnter: (to, from, next) => {
            if (GetCookie('access')) next('/rating')
            else next()
        },
    },
    {
        path: '/rating',
        name: 'rating',
        component: Rating,
        beforeEnter: (to, from, next) => {
            if (!GetCookie('access')) next('/auth')
            else next()
        },
    },
    {
        path: '/applications',
        name: 'applications',
        component: Applications,
        beforeEnter: (to, from, next) => {
            if (!GetCookie('access')) next('/auth')
            else next()
        },
    },
    {
        path: '/applications/create',
        name: 'application-create',
        component: ApplicationCreate,
        beforeEnter: (to, from, next) => {
            if (!GetCookie('access')) next('/auth')
            else next()
        },
    },
    {
        path: '/application/:id',
        name: 'application',
        component: Application,
        beforeEnter: (to, from, next) => {
            if (!GetCookie('access')) next('/auth')
            else next()
        },
    },
    {
        path: '/events',
        name: 'events',
        component: Events,
        beforeEnter: (to, from, next) => {
            if (!(JWTDecode(GetCookie('access')).is_staff || JWTDecode(GetCookie('access')).is_superuser)) next('/auth')
            else next()
        },
    },
    {
        path: '/events/create',
        name: 'event-create',
        component: EventCreate,
        beforeEnter: (to, from, next) => {
            if (!(JWTDecode(GetCookie('access')).is_staff || JWTDecode(GetCookie('access')).is_superuser)) next('/auth')
            else next()
        },
    },
    {
        path: '/event/:id',
        name: 'event',
        component: Event,
        beforeEnter: (to, from, next) => {
            if (!(JWTDecode(GetCookie('access')).is_staff || JWTDecode(GetCookie('access')).is_superuser)) next('/auth')
            else next()
        },
    },
    {
        path: '/:username',
        name: 'profile',
        component: Profile,
        beforeEnter: (to, from, next) => {
            if (!GetCookie('access')) next('/auth')
            else next()
        },
    },
    {
        path: '/settings',
        name: 'settings',
        component: Settings,
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
