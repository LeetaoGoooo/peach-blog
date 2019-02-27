<template>
  <v-app flat="true">
    <sider-bar></sider-bar>
    <v-content>
         <v-container fluid fill-height>
      <post-view :post="post"></post-view>
         </v-container>
    </v-content>
    <peach-footer></peach-footer>
  </v-app>
</template>
<script>
import SiderBar from "@/components/SiderBar";
import PeachFooter from "@/components/Footer";
import PostView from "@/components/PostDetail";
import { getPostDetailByTitle } from "@/api/article";
export default {
  data() {
    return {
      post: {}
    };
  },
  components: { SiderBar, PeachFooter, PostView },
  beforeCreate: function() {
    let title = this.$route.params.title;
    getPostDetailByTitle(title).then(response => {
      console.log(response.data);
      this.post = response.data;
    });
  }
};
</script>
