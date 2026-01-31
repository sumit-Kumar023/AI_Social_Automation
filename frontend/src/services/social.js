import api from "./api";

export const connectSocialAccount = async () => {
  const res = await api.get("/social/connect");
  return res.data;
};
