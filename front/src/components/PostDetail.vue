<template>
    <v-layout>
        <v-flex xs12 sm6 offset-sm3>
            <v-card>
                <v-img src="https://cdn.vuetifyjs.com/images/cards/desert.jpg" aspect-ratio="2.75"></v-img>

                <v-card-title primary-title>
                    <div>
                        <h3 class="headline mb-0">{{post.title}}</h3>
                        <div> {{ post.content }} </div>
                    </div>
                </v-card-title>
            </v-card>
        </v-flex>
    </v-layout>
</template>

<script>
    import {getPostDetailByTitle} from '@/api/article'

    export default {
        data() {
            return {
                post: {},
            }
        },
        beforeCreate: function () {
            let title = this.$router.params
            getPostDetailByTitle(title).then(response =>{
                this.post = response.data 
            })
        }
    }
</script>