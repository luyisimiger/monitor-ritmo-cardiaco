var mutations = {
  SET_SESSIONS(state, data) {
    state.sessions = data;
    console.log(data);
  }
};

export default mutations;
