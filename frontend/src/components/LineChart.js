import { Line, mixins } from "vue-chartjs";
import "chartjs-plugin-streaming";

export default {
  extends: Line,
  mixins: [mixins.reactiveProp],
  props: {
    pause: {
      type: Boolean,
      default: false
    },
    options: {
      type: Object,
      default: null
    }
  },
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
  methods: {
    update() {
      this.$data._chart.update({
        preservation: true
      });
    }
  }
};
