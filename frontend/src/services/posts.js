import api from "./api";

export const createPost = async (postData) => {
  const res = await api.post("/posts/", postData);
  return res.data;
};

export const getPosts = async () => {
  const res = await api.get("/posts/");
  return res.data;
};
