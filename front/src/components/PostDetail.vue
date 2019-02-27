<template>
  <v-layout>
    <v-flex>
      <v-card>
        <v-img src="https://cdn.vuetifyjs.com/images/cards/desert.jpg" aspect-ratio="2.75"></v-img>
        <v-card-title primary-title>
          <div>
            <h3 class="headline mb-0">{{post.title}}</h3>
            <div>
                <!-- {{ post.content }} -->
              <vue-markdown>{{ post.content }}</vue-markdown>
            </div>
          </div>
        </v-card-title>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import VueMarkdown from "vue-markdown";

export default {
  data() {
    return {};
  },
  props: ["post"],
  components: { VueMarkdown }
};
</script>