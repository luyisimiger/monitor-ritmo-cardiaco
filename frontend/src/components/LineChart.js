import { Line } from "vue-chartjs";
import "chartjs-plugin-streaming";

export default {
  extends: Line,
  props: {
    chartData: {
      type: Array,
      default: null
    },
    startdate: Number,
    pause: Boolean
  },

  data: () => ({
    options: {
      title: {
        display: true,
        text: "Monitor del ritmo cardiaco"
      },
      plugins: {
        streaming: {
          frameRate: 30,
          duration: 30000,
          /* delay: 4000,
          refresh: 3000,
          ttl: 60000, */
          pause: false,
          onRefresh: chart => {
            let data = chart.data.datasets[0].data;
            if (data.length <= 5) {
              chart.options.plugins.streaming.pause = true;
            }
          }
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
  }),
  computed: {
    configData() {
      return {
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
      };
    }
  },
  mounted() {
    this.renderChart(this.configData, this.options);
  },
  methods: {
    update() {
      this.$data._chart.update({ preservation: true });
    },
    reset() {
      let chart = this.$data._chart;
      let delay = Date.now() - this.startdate + 35000;
      let newData = this.chartData.map(m => m);

      this.options.plugins.streaming.delay = delay;
      this.options.plugins.streaming.pause = false;
      chart.options = this.options;
      chart.data.datasets[0].data = newData;
      this.update();
    }
  },
  watch: {
    chartData: function() {
      this.reset();
    },
    pause: function() {
      let chart = this.$data._chart;
      let opts = chart.options;
      opts.plugins.streaming.pause = this.pause;
      this.update();
    }
  }
};
