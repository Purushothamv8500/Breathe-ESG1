import axios from "axios";

// Direct production URL; set VITE_API_BASE_URL for overrides
const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  "https://breathe-esg1.onrender.com/api";
  
export function getClientId() {
  return localStorage.getItem("client_id") || "acme";
}

export function setClientId(id) {
  localStorage.setItem("client_id", id);
}

const http = axios.create({
  baseURL: API_BASE,
});

// attach required client_id as a query param to bypass CORS preflight header block
http.interceptors.request.use((config) => {
  config.params = config.params || {};
  config.params.client_id = getClientId();
  return config;
});

export const api = {
  dashboard: () => http.get("/dashboard/").then((r) => r.data),

  records: (params = {}) =>
    http.get("/records/", { params }).then((r) => r.data),

  record: (id) =>
    http.get(`/records/${id}/`).then((r) => r.data),

  approve: (id, body = {}) =>
    http.post(`/records/${id}/approve/`, body).then((r) => r.data),

  reject: (id, body = {}) =>
    http.post(`/records/${id}/reject/`, body).then((r) => r.data),
};

export function unwrapRecords(data) {
  return data?.results ?? data ?? [];
}