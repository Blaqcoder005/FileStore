import Uploads from "./Uploads";
import { useState } from "react";
import { Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Upload, Download, Trash2 } from "lucide-react";

export default function Topbar() {
  const [uploadOpen, setUploadOpen] = useState(false);
  const { user } = useAuth();
  const [activeModal, setActiveModal] = useState(null);
  const closeModal = () => setActiveModal(null);

  return (
    <div className="flex flex-col w-full">
      <div className="flex items-center border-b border-teal-100 bg-dark text-white px-4 py-3">
	<button
	  onClick={() => setActiveModal("upload")}
	  className="flex items-center gap-2 bg-primary hover:bg-primary-hover text-white rounded-lg px-4 py-2"
	>
	  <Upload className="w-4 h-4" />
	  Upload
	</button>
        {uploadOpen && <Upload />}
        <div className="ml-auto">{user?.username}</div>
      </div>
      <div className="flex-1 overflow-y-auto">
        <Outlet />
      </div>
    </div>
  );
}
