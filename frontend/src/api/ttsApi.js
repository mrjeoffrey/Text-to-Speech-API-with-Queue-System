import axios from "axios";

const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const submitTTSRequest = async (data) => {
  const response = await apiClient.post("/tts", data);
  return response.data;
};
