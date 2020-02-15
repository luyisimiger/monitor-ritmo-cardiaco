<template>
  <v-container fluid fill-height>
    <v-toolbar flat>
      <v-spacer></v-spacer>
      <v-toolbar-title class="display-1">Session # {{session.id}}
        <v-btn depressed large :color="session.status == 'open' ? 'green' : 'red'" class="white--text">{{session.status}}</v-btn>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="success" @click="$refs.mychart.reset()">
        <v-icon>mdi-restart</v-icon>
        Reiniciar streaming
      </v-btn>
      <v-btn color="primary">
        <v-icon>mdi-stop</v-icon>
        Detener captura
      </v-btn>
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
                :chartData="chartData"
                :startdate="startdate"
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
    chartData: [],
    startdate: 0,
    requestDataId: null,
    capture: false,
    headers: [
      { text: "Fecha", value: "fecha" },
      { text: "RH", value: "rh" },
      { text: "RR", value: "rr" }
    ]
  }),

  methods: {
    updateChartData() {
      this.chartData = this.session.meditions.map(m => {
        return {
          t: new Date(m.date),
          y: m.rh
        }
      });
      this.startdate = this.session.detail.datestart;
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
        fecha: moment(m.date).format("D MMM YYYY, hh[:]mm[:]ss A")
      }));
      return session;
    },
    startCapture() {
      this.capture = true;
      this.scheduleRequest();
    },
    stopCapture() {
      this.capture = false;
      clearTimeout(this.requestDataId);
    },
    scheduleRequest() {
      if (this.capture) {
        let timeout = 3000;
        this.requestDataId = setTimeout(this.requestData, timeout);
      }
    },
    requestData() {
      this.fetch_session()
        .then(this.updateChartData)
        //.then(vm.scheduleRequest)
        //.catch(vm.scheduleRequest);
    }
  },
  computed: {},
  watch: {},
  created() {
    this.requestData();
  }
};
</script>
