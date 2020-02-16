<template>
  <v-container align-center justify-center>
    <v-row>
      <v-col cols="12">
        <v-toolbar flat>

          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn x-large icon color="primary" v-on="on" @click="fetch_session" :loading="sessions_loading">
                <v-icon>mdi-refresh</v-icon>
              </v-btn>
            </template>
            <span>Actualizar</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn x-large icon color="primary" v-on="on" @click="open">
                <v-icon>mdi-plus-circle</v-icon>
              </v-btn>
            </template>
            <span>Nueva</span>
          </v-tooltip>

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
                  <v-card-title class="">Session # {{ s.id }}
                    <v-spacer></v-spacer>
                    <v-btn text :color="s.status == 'open' ? 'green' : 'red'">{{ s.status }}</v-btn>
                  </v-card-title>
                  <v-card-subtitle>{{ s.meditions.length }} meditions</v-card-subtitle>
                  <v-card-actions>
                    <v-btn text color="primary" :to="{ name: 'sessions-detail', params: { id: s.id }}">detalle</v-btn>
                    <v-btn text color="green" @click="capture(s.id)" v-if="s.status == 'close'">Capture</v-btn>
                    <v-btn text color="danger" @click="close(s.id)" v-if="s.status == 'open'">Close</v-btn>
                    <v-btn text color="red" @click="remove(s.id)" v-if="s.status == 'close'">Remove</v-btn>
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
import service from '@/services/sessions';

export default {
  data: () => ({}),
  computed: mapState(["sessions", "sessions_loading"]),
  methods: {
    ...mapActions(["fetch_session"]),
    open() {
      service.open()
        .then(this.fetch_session);
    },
    capture(id) {
      service.capture(id)
        .then(this.fetch_session);
    },
    close(id) {
      service.close(id)
        .then(this.fetch_session);
    },
    remove(id) {
      service.remove(id)
        .then(this.fetch_session);
    }
  },
  created() {
    this.fetch_session();
  }
};
</script>
