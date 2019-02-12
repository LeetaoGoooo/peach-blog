<template>
  <div class="home">
    <HeaderBar title="PeachBlog"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HeaderBar from '@/components/HeaderBar.vue'

export default {
  name: 'home',
  components: {
    HeaderBar
  }
}
</script>
