import Sessions from "../views/Sessions.vue";
import SessionDetail from "../views/SessionDetail.vue";
import Monitor from "../views/Monitor.vue";

const sessions_routes = [
  {
    path: "/sessions",
    name: "sessions-list",
    component: Sessions
  },
  {
    path: "/session/open",
    name: "sessions-open",
    component: Monitor
  },
  {
    path: "/session/:id/detail",
    name: "sessions-detail",
    component: SessionDetail,
    props: true
  }
];

export default sessions_routes;
