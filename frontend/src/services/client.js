import axios from "axios";

export const api = axios.create({
  baseURL: "/api",
  withCredentials: true,
});

export const listFiles = (folderId) =>
  api.get("/files/files", { params: { folder_id: folderId } }).then(r => r.data);

export const uploadFile = (file, folderId, onProgress) => {
  const fd = new FormData();
  fd.append("file", file);
  if (folderId) fd.append("folder_id", folderId);
  return api.post("/files/upload", fd, {
    onUploadProgress: e => onProgress?.(Math.round((e.loaded * 100) / e.total)),
  });
};
