import request from '@/utils/request'

export function getPostListByPage() {
    let url = '/';
    if (arguments[0] != 'undefined') {
        url = '/?page=' + arguments[0]
    }
    return request({
        url: url,
        method: 'get'
    })
}

export function getPostDetailByTitle(title) {
    let url = '/post/' + title
    return request({
        url: url,
        method: 'get'
    })
}