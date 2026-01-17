// lib/api.js
import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const analyzeProduct = async (url, token) => {
  const response = await axios.post(
    `${API_BASE_URL}/analyze`,
    {
      product_url: url,
      force_refresh: false,
    },
    {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    },
  );

  return response.data;
};
