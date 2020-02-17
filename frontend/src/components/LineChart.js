import { Line } from "vue-chartjs";
import "chartjs-plugin-streaming";

const DURATION = 30000;

const charOpts = {
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
        id: "y-axis-1",
        type: "linear",
        display: true,
        scaleLabel: {
          display: true,
          labelString: "values (rh)"
        }
      },
      {
        id: "y-axis-2",
        type: "linear",
        display: true,
        position: "right",
        scaleLabel: {
          display: true,
          labelString: "values (rr)"
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
};

export default {
  extends: Line,
  props: {
    chartDataRH: {
      type: Array,
      default: null
    },
    chartDataRR: {
      type: Array,
      default: null
    },
    startdate: Number,
    enddate: Number,
    pause: Boolean,
    applyDelay: Boolean
  },

  data() {
    let vm = this;    
    return {
      started: false,
      options: {
        title: {
          display: true,
          text: "Monitor del ritmo cardiaco"
        },
        plugins: {
          streaming: {
            frameRate: 30,
            duration: DURATION,
            /* delay: 4000,
            refresh: 3000,
            ttl: 60000, */
            pause: false,
            onRefresh: chart => {
              let delay = chart.options.plugins.streaming.delay;
              let now = Date.now() - delay;
              let pause = false;
              if (now - vm.enddate >= (0.5 * DURATION)) pause = true;

              chart.options.plugins.streaming.pause = pause;
            }
          }
        },
        ...charOpts
      }
    };
  },
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
            data: [],
            yAxisID: "y-axis-1"
          },
          {
            label: "Variabilidad ritmo cardiaco",
            backgroundColor: "blue",
            borderColor: "blue",
            cubicInterpolationMode: "monotone",
            fill: false,
            lineTension: 1.2,
            data: [],
            yAxisID: "y-axis-2"
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
    updateChartData() {
      let chart = this.$data._chart;
      let newDataRH = this.chartDataRH.map(m => m);
      let newDataRR = this.chartDataRR.map(m => m);

      chart.data.datasets[0].data = newDataRH;
      chart.data.datasets[1].data = newDataRR;
      this.update();
    },
    updateDelay(delay) {
      let chart = this.$data._chart;
      this.options.plugins.streaming.delay = delay;
      chart.options = this.options;
      this.update();
    },
    reset() {
      let chart = this.$data._chart;
      this.options.plugins.streaming.pause = false;

      if (this.applyDelay) {
        let delay = Date.now() - this.startdate;
        this.options.plugins.streaming.delay = delay;
        this.updateDelay(delay);
      }      
      
      chart.options = this.options;
      this.updateChartData();
    },
    start() {
      if (!this.started) {
        this.started = true;
        this.reset();
      } else {
        this.updateChartData();
      }
    }
  },
  watch: {
    chartDataRH: function() {
      this.start();
    },
    chartDataRR: function() {
      this.start();
    },
    applyDelay() {
      console.log("applyDelay");
      if (!this.applyDelay) this.updateDelay(0);
    },
    pause: function() {
      let chart = this.$data._chart;
      let opts = chart.options;
      opts.plugins.streaming.pause = this.pause;
      this.update();
    }
  }
};
