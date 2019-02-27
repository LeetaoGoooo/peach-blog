<template>
  <v-container grid-list-md text-xs-center>
    <v-layout>
      <v-flex xs12 sm6 offset-sm3>
        <v-card>
          <v-card-title primary-title>
            <div>
              <h3 class="headline mb-0">Peach Blog Login</h3>
              <div>
                <v-form ref="form" lazy-validation>
                  <v-container>
                    <v-layout row wrap>
                      <v-flex xs12>
                        <v-text-field
                          prepend-icon="face"
                          v-model="name"
                          :counter="10"
                          :rules="nameRules"
                          label="Name"
                          required
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs12>
                        <v-text-field
                          prepend-icon="lock"
                          v-model="password"
                          :rules="pwdRules"
                          label="Password"
                          type="password"
                          required
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm12>
                        <v-btn color="success" @click="validate">Login</v-btn>
                      </v-flex>
                    </v-layout>
                  </v-container>
                </v-form>
              </div>
            </div>
          </v-card-title>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    name: "",
    nameRules: [
      v => !!v || "Name is required",
      v => (v && v.length <= 10) || "Name must be less than 10 characters"
    ],

    password: "",
    pwdRules: [
      v => !!v || "Password is required",
      v => (v && v.length > 6) || "Password must be less than 6 characters"
    ]
  }),

  methods: {
    validate() {
      if (this.$refs.form.validate()) {
        //
      }
    }
  }
};
</script>