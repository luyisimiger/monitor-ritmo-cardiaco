import axios from '../axios';

const open = () => {
  return axios.get("/sessions/open");
}

const close = (id) => {
  let url = `/sessions/${id}/close`
  return axios.get(url);
}

const detail = (id) => {
  let url = `/sessions/${id}/detail`
  return axios.get(url);
}

const fetch = () => {
  return axios.get("/sessions");
}

export default {
  open,
  close,
  detail,
  fetch
}
