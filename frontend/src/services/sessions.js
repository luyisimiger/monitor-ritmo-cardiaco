import axios from '../axios';

const open = () => {
  return axios.get("/sessions/open");
}

const capture = (id) => {
  let url = `/sessions/${id}/capture`
  return axios.get(url);
}

const close = (id) => {
  let url = `/sessions/${id}/close`
  return axios.get(url);
}

const remove = (id) => {
  let url = `/sessions/${id}/remove`
  return axios.get(url);
}

const detail = (id) => {
  let url = `/sessions/${id}/detail`
  return axios.get(url);
}

const fetch = () => {
  return axios.get("/sessions/full");
}

export default {
  open,
  capture,
  close,
  remove,
  detail,
  fetch
}
