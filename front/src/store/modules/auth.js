import request from '@/utils/request'


export function loginByUserName(username, password) {
    const formData = {
        "username": username,
        "password": password
    }
    return request({
        url: '/api/auth/login',
        method: 'post',
        formData
    })
}

export function logout() {
    return request({
        url: '/api/auth/logout',
        method: 'post'
    })
}