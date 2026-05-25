import axios from "axios";

// Relative /api uses Vite proxy in dev; set VITE_API_BASE_URL for production
const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  "https://breathe-esg-1hc4.onrender.com/api";
  
export function getClientId() {
  return localStorage.getItem("client_id") || "acme";
}

export function setClientId(id) {
  localStorage.setItem("client_id", id);
}

const http = axios.create({
  baseURL: API_BASE,
});

// attach required header
http.interceptors.request.use((config) => {
  config.headers["X-Client-Id"] = getClientId();
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