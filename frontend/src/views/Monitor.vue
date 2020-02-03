<template>
  <div class="graficca">
    <h1>Chart.js</h1>
    <LineChart
      ref="mychart"
      :chartData="config.data"
      :options="config.options"
    />
  </div>
</template>

<script>
// @ is an alias to /src
import LineChart from "@/components/LineChart.js";
import axios from "axios";

export default {
  name: "monitor",
  components: {
    LineChart
  },
  data: () => ({
    chart: null,
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
                duration: 30000,
                delay: 5000,
                refresh: 1000,
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
                labelString: "value"
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

  mounted() {
    this.startCapture();
  },

  methods: {
    doPulse(pulse) {
      let dataset = this.config.data.datasets[0];
      dataset.data.push({
        x: Date.now(),
        y: pulse
      });

      this.$refs.mychart.update();
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
        let timeout = 3000; //random.int(1000, 3000);
        this.requestDataId = setTimeout(this.requestData, timeout);
      }
    },

    requestData() {
      let vm = this;
      axios.defaults.baseURL = process.env.VUE_APP_URL_SERVICE;
      axios
        .get("/device/readdata")
        .then(vm.receiveData)
        .catch(vm.scheduleRequest);
    },

    receiveData(response) {
      let rh = response.data.rh;
      this.doPulse(rh);
      this.scheduleRequest();
    }
  },
  computed: {},
  watch: {}
};
</script>
