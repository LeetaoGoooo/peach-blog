<template>
  <v-app flat=true>
    <sider-bar></sider-bar>
    <v-content>
       <post-list :posts='posts'></post-list>
       <pageination :total_page="total_page" v-model="page"></pageination>
    </v-content>
    <peach-footer></peach-footer>
  </v-app>
</template>

<script>
 import SiderBar from '@/components/SiderBar'
 import PostList from '@/components/PostList'
 import Pageination from '@/components/Pageination'
 import PeachFooter from '@/components/Footer'

 import {getPostListByPage} from '@/api/article'

  export default {
    data: () => ({
      drawer: null,
      page:1,
      posts: {},
      total_page:0
    }),
    components:{ PostList, Pageination,PeachFooter,SiderBar},
    watch:{
      page(new_page) {
        this.getPostsByPage(new_page)
      }
    },
    created() {
      this.getPostsByPage(1)
    },
    methods:{
      getPostsByPage(current_page) {
        getPostListByPage(current_page).then(response => {
           this.posts = response.data.posts
           this.total_page = parseInt(response.data.total_page)
        })
      }
    }
  }
</script>