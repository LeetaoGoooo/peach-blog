<template>
    <v-card>
        <v-container fluid grid-list-lg>
            <v-layout row wrap v-for="post in posts" :key="post.title">
                <v-flex xs12>
                    <v-card>
                        <v-card-title primary-title>
                            <div>
                                <div class="headline">{{post.title}}</div>
                                <span>
                                    <!-- content -->
                                </span>
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