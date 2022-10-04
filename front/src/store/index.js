import { createStore } from 'vuex'


import { SetCookie, GetCookie } from '@/utils/cookie.js'
import { POST, GET } from '@/utils/fetch.js'



export default createStore({
    state: {
        // url: '',
        // json: '',
    },
    getters: {},
    mutations: {
        // IsAuth() {
        //     if (GetCookie('refresh') && !GetCookie('access')) this.UpdateToken()
        //     if (!GetCookie('refresh') && !GetCookie('access')) this.$router.push('/auth')
        // },
        // async UpdateToken(state) {
        //     const url = `token/refresh`
        //     const json = {
        //         refresh: GetCookie('refresh')
        //     }

        //     const response = await POST(url, json)

        //     if (response.status === 200) {
        //         SetCookie('access', response.data.access, JWTDecode(response.data.access).exp, 'y')

        //         const response = await GET(state.ur)
        //     }
        // },
    },
    actions: {},
    modules: {}
})
