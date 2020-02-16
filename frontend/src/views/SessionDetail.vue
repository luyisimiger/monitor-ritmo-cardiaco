<template>
  <v-container fluid fill-height>
    <v-toolbar flat>
      
      <v-toolbar-title>
        Session # {{session.id}}
        <v-btn depressed small :color="session.status == 'open' ? 'green' : 'red'" class="white--text">{{session.status}}</v-btn>
      </v-toolbar-title>
      
      <v-spacer></v-spacer>

      <v-btn text color="success" v-if="!capture" @click="$refs.mychart.reset()">
        <v-icon>mdi-restart</v-icon>
        Reiniciar streaming
      </v-btn>
      
      <v-btn text color="primary" v-if="!capture" @click="startCapture">
        <v-icon>mdi-play</v-icon>
        Iniciar captura
      </v-btn>
      
      <v-btn text color="primary" v-if="capture" @click="stopCapture">
        <v-icon>mdi-stop</v-icon>
        Detener captura
      </v-btn>

      <v-spacer></v-spacer>

      <v-toolbar-title class="overline">
        {{session.meditions.length}} meditions
      </v-toolbar-title>

      <v-spacer></v-spacer>

    </v-toolbar>
    <v-row align="center" justify="center">
      <v-col cols="12">
        <v-tabs v-model="tab" :centered="true" :icons-and-text="true">
          <v-tab key="grafica">Grafica<v-icon>mdi-chart-line</v-icon></v-tab>
          <v-tab key="data">Datos tabulados<v-icon>mdi-table-large</v-icon></v-tab>
        </v-tabs>
      </v-col>
    </v-row>
    <v-row align="center" justify="center">
      <v-col cols="5">
        <v-tabs-items v-model="tab"
          cycle
          touchless
        >
          <v-tab-item
            key="grafica"
          >
            <v-responsive aspect-ratio="1">
              <LineChart
                ref="mychart"
                :chartDataRH="chartDataRH"
                :chartDataRR="chartDataRR"
                :startdate="startdate"
                :enddate="enddate"
                :applyDelay="!capture"
              />
            </v-responsive>
          </v-tab-item>
          <v-tab-item
            key="data"
          >
            <v-data-table
              :headers="headers"
              :items="session.meditions"
            >
            </v-data-table>
          </v-tab-item>
        </v-tabs-items>
      </v-col>
      <v-col cols="2">
        <v-row>
          <v-col md>
            <v-card>
              <v-list color="red" dense>
                <v-subheader class="headline white--text">DATOS DEL RH</v-subheader>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title class="title white--text">{{ session.detail.rh.average }}</v-list-item-title>
                    <v-list-item-subtitle class="white--text">Valor Promedio</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title class="title white--text">{{ session.detail.rh.max }}</v-list-item-title>
                    <v-list-item-subtitle class="white--text">Valor Maximo</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title class="title white--text">{{ session.detail.rh.min }}</v-list-item-title>
                    <v-list-item-subtitle class="white--text">Valor Minimo</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title class="title white--text">{{ session.detail.rh.sigma }}</v-list-item-title>
                    <v-list-item-subtitle class="white--text">Desviacion estandar</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>
        </v-row>
        <v-row>
          <v-col md>
            <v-card>
              <v-list color="blue" dense>
                <v-subheader class="headline white--text">DATOS DEL RR</v-subheader>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title class="title white--text">{{ session.detail.rr.average }}</v-list-item-title>
                    <v-list-item-subtitle class="white--text">Valor Promedio</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title class="title white--text">{{ session.detail.rr.max }}</v-list-item-title>
                    <v-list-item-subtitle class="white--text">Valor Maximo</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title class="title white--text">{{ session.detail.rr.min }}</v-list-item-title>
                    <v-list-item-subtitle class="white--text">Valor Minimo</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title class="title white--text">{{ session.detail.rr.sigma }}</v-list-item-title>
                    <v-list-item-subtitle class="white--text">Desviacion estandar</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// @ is an alias to /src
import LineChart from "@/components/LineChart.js";
import service from "@/services/sessions";
import moment from "moment";

export default {
  components: {
    LineChart
  },

  props: {
    id: {
      type: String,
      required: true
    }
  },
  data: () => ({
    tab: null,
    session: {
      id: 0,
      status: "",
      detail: {
        rh: {
          average: 0,
          max: 0,
          min: 0,
          sigma: 0
        },
        rr: {
          average: 0,
          max: 0,
          min: 0,
          sigma: 0
        }
      },
      meditions: []
    },
    requestDataId: null,
    headers: [
      { text: "Fecha", value: "fecha" },
      { text: "RH", value: "rh" },
      { text: "RR", value: "rr" }
    ]
  }),

  computed: {
    chartDataRH() {
      return this.session.meditions.map(m => {
        return {
          t: new Date(m.date),
          y: m.rh
        }
      });      
    },
    chartDataRR() {
      return this.session.meditions.map(m => {
        return {
          t: new Date(m.date),
          y: m.rr
        }
      });      
    },
    capture() {
      return this.session.status == "open";
    },
    startdate() {
      return this.session.detail.datestart;
    },
    enddate() {
      return this.session.detail.dateend;
    }
  },

  methods: {
    strDate(date) {
      return moment(date).format("D MMM YYYY, hh[:]mm[:]ss A")
    },
    fetch_session() {
      let vm = this;
      return service.detail(vm.id)
        .then(response => {
          vm.session = vm.parse_session(response.data);
        });
    },
    parse_session(session) {
      session.meditions = session.meditions.map(m => ({
        ...m,
        fecha: this.strDate(m.date)
      }));
      return session;
    },
    startCapture() {
      service.capture(this.session.id)
        .then(this.requestData);
    },
    stopCapture() {
      clearTimeout(this.requestDataId);
      service.close(this.session.id)
        .then(this.requestData);
    },
    scheduleRequest() {
      if (this.capture) {
        let timeout = 3000;
        clearTimeout(this.requestDataId);
        this.requestDataId = setTimeout(this.requestData, timeout);
      }
    },
    requestData() {
      this.fetch_session()
        .then(this.scheduleRequest)
        .catch(this.scheduleRequest);
    }
  },
  watch: {},
  created() {
    this.requestData();
  }
};
</script>
