import axios from 'axios'
/** TODO */
// import store import '@/store'

// import { getToken } from '@/utils/auth'

const service = axios.create({
    baseURL: 'http://localhost:5000',
    timeout: 5000
})

service.interceptors.request.use(
    // config => {
    //     if (store.getters.token) {
    //         config.headers['authentication'] = getToken()
    //     }
    //     return config
    // },
    // error => {
    //     console.log(error)
    //     Promise.reject(error)
    // }
)

service.interceptors.response.use(
    response => response,
    /**
  * 下面的注释为通过在response里，自定义code来标示请求状态
  * 当code返回如下情况则说明权限有问题，登出并返回到登录页
  * 如想通过 xmlhttprequest 来状态码标识 逻辑可写在下面error中
  * 以下代码均为样例，请结合自生需求加以修改，若不需要，则可删除
  */
    // response => {
    //   const res = response.data
    //   if (res.code !== 20000) {
    //     Message({
    //       message: res.message,
    //       type: 'error',
    //       duration: 5 * 1000
    //     })
    //     // 50008:非法的token; 50012:其他客户端登录了;  50014:Token 过期了;
    //     if (res.code === 50008 || res.code === 50012 || res.code === 50014) {
    //       // 请自行在引入 MessageBox
    //       // import { Message, MessageBox } from 'element-ui'
    //       MessageBox.confirm('你已被登出，可以取消继续留在该页面，或者重新登录', '确定登出', {
    //         confirmButtonText: '重新登录',
    //         cancelButtonText: '取消',
    //         type: 'warning'
    //       }).then(() => {
    //         store.dispatch('FedLogOut').then(() => {
    //           location.reload() // 为了重新实例化vue-router对象 避免bug
    //         })
    //       })
    //     }
    //     return Promise.reject('error')
    //   } else {
    //     return response.data
    //   }
    // },
    error => {
        console.log('err' + error) // for debug
        // Message({
        //     message: error.message,
        //     type: 'error',
        //     duration: 5 * 1000
        // })
        return Promise.reject(error)
    }
)

export default service