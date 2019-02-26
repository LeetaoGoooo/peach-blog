<template>
  <v-app flat=true>
    <v-navigation-drawer v-model="drawer" fixed app>
      <v-card class="mx-auto">
          <v-img :aspect-ratio="16/9" src="https://cdn.vuetifyjs.com/images/parallax/material.jpg">
            <v-layout pa-2 column fill-height class="lightbox white--text">
              <v-spacer></v-spacer>
              <v-flex shrink>
                <div class="subheading">Leetao</div>
                <div class="body-1">leetao94cn@gmail.com</div>
              </v-flex>
            </v-layout>
          </v-img>
      </v-card>
      <v-list>
        <v-list-tile @click="">
          <v-list-tile-action>
            <v-icon>home</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>Home</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile @click="">
          <v-list-tile-action>
            <v-icon>contact_mail</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>Contact</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar color="indigo" dark fixed app>
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      <v-toolbar-title>PeachBlog</v-toolbar-title>
    </v-toolbar>
    <v-content>
       <post-list :posts='posts'></post-list>
      <div class="text-xs-center">
        <v-pagination
          v-model="page"
          :length="total_page"
          :total-visible="7"
        ></v-pagination>
      </div>
    </v-content>
    <v-footer color="indigo" app>
      <span class="white--text">&copy; 2017</span>
    </v-footer>
  </v-app>
</template>

<script>
 import PostList from '@/components/PostList'
 import {getPostListByPage} from '@/api/article'

  export default {
    data: () => ({
      drawer: null,
      posts: {},
      page:1,
      total_page:0
    }),
    components:{ PostList},
    watch:{
      page:function(new_page, old_page) {
        getPostListByPage(new_page).then(response => {
           console.log(response.data)
           this.posts = response.data.posts
           this.total_page = parseInt(response.data.total_page)
        })
      }
    },
    created() {
      this.getPostList()
    },
    methods:{
      getPostList() {
        getPostListByPage(1).then(response => {
           console.log(response.data)
           this.posts = response.data.posts
           this.total_page = parseInt(response.data.total_page)
           this.current_page = parseInt(response.data.current_page)
        })
      }
    }
  }
</script>