<template>
  <div class="text-xs-center">
    <v-pagination
      v-model="page"
      :value="current_page"
      :length="total_page"
      :total-visible="7"
    ></v-pagination>
  </div>
</template>

<script>
export default {
    data: () => ({
        page:1
    }),
    props:{
        total_page:Number,
        current_page: Number
    }
}
</script>
