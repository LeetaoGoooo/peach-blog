<template>
  <div class="text-xs-center">
    <v-pagination
      :value="page"
      v-model="current_page"
      :length="total_page"
      :total-visible="7"
      @input="handleInputChange"
    ></v-pagination>
  </div>
</template>

<script>
export default {
    data () {
      return {
        current_page:this.page || 1
      }
    },
    props:{
        total_page:Number,
        page:Number
    },
    methods:{
      handleInputChange(new_page) {
        this.$emit('input', new_page)
      }
    }
}
</script>
