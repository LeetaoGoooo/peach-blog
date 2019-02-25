import request from '@/utils/request'

export function getPostListByPage() {
    var url = '/';
    if (arguments[0] != 'undefined') {
        url = '/?page=' + arguments[0]
    } 
    return request({
        url: url,
        method:'get'
    })
}