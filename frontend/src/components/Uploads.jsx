import { useState } from "react";
import { uploadFile } from "../services/client";
import Modal from "./modals/Modal";

export default function FileImport({ onClose, onUploaded }) {
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState("");

  const handleFile = async (file) => {
    if (!file || loading) return;
    setLoading(true);
    setError("");
    try {
      await uploadFile(file, null, setProgress);
      onUploaded?.();
      onClose();
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Upload failed");
    } finally {
      setLoading(false);
      setProgress(0);
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    handleFile(e.dataTransfer.files[0]);
  };

  const safeClose = () => {
    if (!loading) onClose();
  };

  return (
    <Modal title="Upload file" onClose={safeClose}>
      {error && (
        <div className="mb-3 bg-red-50 border border-red-300 text-red-700 px-3 py-2 rounded-lg text-sm">
          {error}
        </div>
      )}

      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        className={`rounded-xl border-2 border-dashed bg-dark p-10 text-center text-white ${
          dragging ? "border-primary bg-primary/10" : "border-tint/40"
        }`}
      >
        <input
          type="file"
          id="fileInput"
          hidden
          onChange={(e) => {
            handleFile(e.target.files[0]);
            e.target.value = "";
          }}
        />
        <label htmlFor="fileInput" className="cursor-pointer">
          {loading ? `Uploading... ${progress}%` : "Drop file here or tap to choose"}
        </label>
      </div>
    </Modal>
  );
}
