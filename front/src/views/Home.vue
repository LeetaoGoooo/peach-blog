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
       <pageination :total_page="total_page" v-model="page"></pageination>
    </v-content>
    <peach-footer></peach-footer>
  </v-app>
</template>

<script>
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
    components:{ PostList, Pageination,PeachFooter},
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