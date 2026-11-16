import { useState } from "react";
import { Outlet } from "react-router-dom";
import Topbar from "./Topbar";
import Upload from "./Uploads";

export default function Layout() {
  const [activeModal, setActiveModal] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const closeModal = () => setActiveModal(null);

  return (
    <div className="min-h-screen bg-surface text-ink">
      <Topbar onUpload={() => setActiveModal("upload")} />

      <main className="p-4">
        <Outlet context={{ refreshKey }} />
      </main>

      {activeModal === "upload" && (
        <Upload
          onClose={closeModal}
          onUploaded={() => setRefreshKey((k) => k + 1)}
        />
      )}
    </div>
  );
}
