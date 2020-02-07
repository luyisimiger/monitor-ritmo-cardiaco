import axios from "@/axios.js";

var actions = {
  fetch_session(context) {
    context.state.sessions_loading = true;
    axios.get("/sessions").then(response => {
      context.state.sessions_loading = false;
      context.commit("SET_SESSIONS", response.data.result);
    }).catch(() => {
      context.state.sessions_loading = false;
    });
  }
};

export default actions;
