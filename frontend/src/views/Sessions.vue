<template>
  <v-container align-center justify-center>
    <v-row>
      <v-col cols="12">
        <v-toolbar flat color="">
          <v-btn outlined color="primary" @click="fetch_session" :loading="sessions_loading">
            <v-icon>mdi-refresh</v-icon>
            actualizar
          </v-btn>
          <v-spacer></v-spacer>
        </v-toolbar>
        
        <v-data-iterator
          content-tag="tag"
          row
          :items="sessions"
        >
          <template v-slot:default="props">
            <v-row>
              <v-col
                v-for="s in props.items"
                :key="s.id"
                cols="12"
                sm="6"
                md="4"
                lg="3"
              >
                <v-card color="">
                  
                  <v-card-title class="headline">Session # {{ s.id }}</v-card-title>
                  
                  <v-card-actions>
                    <v-btn outlined x-small color="red">{{ s.status }}</v-btn>
                    <v-btn outlined x-small color="black">n meditions</v-btn>
                  </v-card-actions>

                  <v-card-actions>
                    <v-btn text color="primary">Ver detalle</v-btn>
                  </v-card-actions>
                
                </v-card>
                
              </v-col>
            </v-row>
          </template>
        </v-data-iterator>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  data: () => ({}),
  computed: mapState(["sessions", "sessions_loading"]),
  methods: {
    ...mapActions(["fetch_session"])
  },
  created() {
    this.fetch_session();
  }
};
</script>
