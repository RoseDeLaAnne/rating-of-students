export const SetCookie = (name, value, expires, secure) => {
    document.cookie = `${name}=${value};${!isNaN(expires) ? ` expires=${new Date(expires * 1000)};` : ``}${secure ? ` Secure;` : ``} path=/`
}

export const DeleteCookie = (name) => {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`
}

export const GetCookie = (name) => {
    var cookie = {}


    document.cookie.split(';').forEach((i) => {
        let [key, value] = i.split('=')

        cookie[key.trim()] = value
    })


    return cookie[name]
}
