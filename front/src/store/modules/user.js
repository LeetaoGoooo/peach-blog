import request from '@/utils/request'


export function getUser() {
    return request({
        url: '/api/user',
        method: 'get'
    })
}

export function updateUser() {
    return request({
        url: 'api/user',
        method: 'post'
    })
}