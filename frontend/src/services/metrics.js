import api from "./api";

export const getMetrics = async (platform) => {
  const res = await api.get(`/monitor/metrics?platform=${platform}`);
  return res.data;
};

