export const POST = async(url, json, access, files) => {
    if (files) {
        var body = new FormData()

        body.append('json', JSON.stringify(json))
        body.append('files', files)


        if (access) {
            var options = {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${access}`
                },
                body: body
            }
        } else {
            var options = {
                method: 'POST',
                headers: {},
                body: body
            }
        }
    } else {
        if (access) {
            var options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${access}`
                },
                body: JSON.stringify(json)
            }
        } else {
            var options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(json)
            }
        }
    }


    const response = await fetch(`/api/${url}/`, options)


    try {
        const data = await response.json()
        const status = response.status


        return { data, status }
    } catch {
        const status = response.status


        return { status }
    }
}

export const GET = async(url, access) => {
    if (access) {
        var options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access}`
            }
        }
    } else {
        var options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }
    }


    const response = await fetch(`/api/${url}/`, options)


    try {
        const data = await response.json()
        const status = response.status


        return { data, status }
    } catch {
        const status = response.status


        return { status }
    }
}
