<template>
  <v-container align-center justify-center>
    <v-row>
      <v-col cols="12">

        <v-toolbar flat>

          <v-toolbar-title>Session # {{session.id}} - {{session.status}}</v-toolbar-title>

          <v-spacer></v-spacer>

          <v-btn flat color="primary">
            <v-icon>mdi-stop</v-icon>
            Detener captura
          </v-btn>

        </v-toolbar>


        <h1>Nueva Sesion</h1>
          <v-tabs
            :centered="true"
            :icons-and-text="true"
          >
            <v-tabs-slider></v-tabs-slider>
            <v-tab>RH<v-icon>mdi-heart-pulse</v-icon></v-tab>
            <v-tab>RR<v-icon>mdi-heart-broken</v-icon></v-tab>
          </v-tabs>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="8" offset="2">
        <LineChart
          ref="mychart"
          :chartData="config.data"
          :options="config.options"
        />
      </v-col>
      <v-col cols="2">
        <v-flex
          align-center
          d-flex
          justify-center
        >
          <v-card
            color="blue"
            replace
            :ripple="false"
            reverse
          >
            <v-list-item>
              <v-list-item-avatar color="grey"></v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title class="headline">Our Changing Planet</v-list-item-title>
                <v-list-item-subtitle>by Kurt Wagner</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-avatar color="grey"></v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title class="headline">Our Changing Planet</v-list-item-title>
                <v-list-item-subtitle>by Kurt Wagner</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-avatar color="grey"></v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title class="headline">Our Changing Planet</v-list-item-title>
                <v-list-item-subtitle>by Kurt Wagner</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-avatar color="grey"></v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title class="headline">Our Changing Planet</v-list-item-title>
                <v-list-item-subtitle>by Kurt Wagner</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-card>
        </v-flex>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// @ is an alias to /src
import LineChart from "@/components/LineChart.js";
import axios from "../axios.js";
import service from "@/services/sessions";

export default {
  name: "monitor",
  components: {
    LineChart
  },

  data: () => ({
    session: {},
    requestDataId: null,
    capture: false,
    config: {
      type: "line",
      data: {
        datasets: [
          {
            label: "Ritmo cardiaco",
            backgroundColor: "red",
            borderColor: "red",
            cubicInterpolationMode: "monotone",
            fill: false,
            lineTension: 1.2,
            data: []
          }
        ]
      },
      options: {
        title: {
          display: true,
          text: "Monitor del ritmo cardiaco"
        },
        plugins: {
          streaming: {
            frameRate: 30
          }
        },
        scales: {
          xAxes: [
            {
              type: "realtime",
              time: {
                displayFormats: {
                  minute: "YYYY-MM-DD h:mm a"
                }
              },
              realtime: {
                duration: 20000,
                delay: 4000,
                refresh: 3000,
                ttl: 60000,
                pause: false
              }
            }
          ],
          yAxes: [
            {
              type: "linear",
              display: true,
              scaleLabel: {
                display: true,
                labelString: "values (rh)"
              },
              ticks: {
                beginAtZero: true
              }
            }
          ]
        },
        tooltips: {
          mode: "nearest",
          intersect: false
        },
        hover: {
          mode: "nearest",
          intersect: false
        }
      }
    }
  }),

  methods: {

    doPulse(pulse) {
      let dataset = this.config.data.datasets[0];
      dataset.data.push({
        x: Date.now(),
        y: pulse
      });

      this.$refs.mychart.update({ preservation: true });
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
      let vm = this;
      axios
        .get("/device/readdata")
        .then(vm.receiveData)
        .catch(vm.scheduleRequest);
    },

    receiveData(response) {
      let rh = response.data.rh;
      console.log(response.data);
      this.doPulse(rh);
      this.scheduleRequest();
    }

  },
  
  computed: {},
  watch: {},

  created() {
    let vm = this;
    service.open()
      .then(response => {
        vm.session = response.data;
      });
  },

  mounted() {
    this.startCapture();
  }
};
</script>
