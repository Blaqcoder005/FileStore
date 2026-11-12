import { useState } from "react";
// import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import { Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext"; // adjust path to wherever this lives

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user } = useAuth();
  const [activeModal, setActiveModal] = useState(null);
  const closeModal = () => setActiveModal(null)

  return (
    <div className="flex min-h-screen bg-surface text-ink">
      <div className="flex flex-1 flex-col">
        <Topbar onUpload={() => setActiveModal("upload")} />

        {activeModal === "upload" && (
          <UploadModal onClose={closeModal} onUploaded={refreshFiles} />
        )}
      </div>
    </div>
  );
}
