import { useState } from "react";
import { uploadFile } from "../services/client";
import Modal from "./Modal";

export default function FileImport({ onUploadDone }) {
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(true);

{/*  const uploadFile = async (file) => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("/api/upload", {
      method: "POST",
      body: formData,
      credentials: "include",
    });

    const data = await res.json();
    if (data.success && onUploadDone) {
      onUploadDone(data.file);
    }
  };*/}

  const onDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) uploadFile(file);
  };

  return (
    
    <Modal 
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60" 
      title="Upload file
      onClose={onClose}
    >
     <div
       onDragOver={(e) => {
         e.preventDefault();
         setDragging(true);
       }}
       onDragLeave={() => setDragging(false)}
       onDrop={onDrop}
       className={`w-[90%] max-w-md rounded-xl border-2 border-dashed bg-dark p-10 text-center text-white mb-30 border-2 border-dashed p-10 rounded-xl text-center ${
         dragging ? "border-primary bg-primary/10" : ""
       }`}
     >
       <input
         type="file"
         onChange={(e) => uploadFile(e.target.files[0])}
         hidden
         id="fileInput"
       />
       <label htmlFor="fileInput" className="cursor-pointer">
         Drop file here or click to upload
       </label>
      </div>
     </Modal>
  );
}
