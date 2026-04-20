import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export const getRULSeries = async (data) => {
  if (data.length < 50) return null;

  const res = await axios.post(`${API_URL}/predict_series`, data);
  return res.data.rul_series;
};