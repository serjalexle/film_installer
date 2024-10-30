import axios from "axios";

export const api = axios.create({
  withCredentials: true,
  baseURL: "https://cffa-93-175-200-53.ngrok-free.app",
  headers: {
    "Content-Type": "application/json",
  },
});

export const tiktok_api = {
  generateContent: async () => {
    return await api.get("/api/citations/generate_content");
  },
};
