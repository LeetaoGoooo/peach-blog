<template>
    <v-card>
        <v-container fluid grid-list-lg>
            <v-layout row wrap v-for="post in posts" :key="post.title">
                <v-flex xs12>
                    <v-card>
                        <v-card-title primary-title>
                            <div>
                                <div class="display-2" style="colro:#9E9E9E"><span style="border: 1px solid #2196F3;margin-right: 5px;"></span>{{post.title}} </div>
                                <div style="margin-top:1rem">
                                    <span class="text-xs-right"><v-icon>calendar_today</v-icon>{{post.create_at}}</span>
                                </div>
                                <div style="margin-top:1rem">
                                    <VueMarkdown>
                                        {{post.content.substring(0,200)}}
                                    </VueMarkdown>
                                </div>
                            </div>
                        </v-card-title>
                        <v-card-actions>
                                <v-btn color="info">阅读更多</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-flex>
            </v-layout>
        </v-container>
    </v-card>
</template>

<script>
  import VueMarkdown from 'vue-markdown'
  
  export default {
    data () {
        page:0
    },
    props:['posts'],
    components:{VueMarkdown}
  }
</script>
