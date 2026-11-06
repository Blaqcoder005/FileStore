import { useEffect, useState } from "react";
// import "../styles/dashboard.css";
import { apiFetch } from "../services/api";
import Topbar from "../components/Topbar";
import { api, listFiles } from "../services/client";
import { useAuth } from "../context/AuthContext";
import FileTile from "../components/FileTile";


export default function Dashboard() {
  const [folder, setFolder] = useState([]);
  const [files, setFiles] = useState([]);
  const { user } = useAuth()

  const handleDownload = (file) => {
    window.location.href = `/api/files/download/${file.id}`;
  };

  const handleDelete = async (file) => {
    if (!window.confirm(`Delete ${file.name}?`)) return;
    await api.delete(`/files/files/${file.id}`);
    setFiles((prev) => prev.filter((x) => x.id !== file.id));
  };

  useEffect(() => {
    let cancelled = false;

    listFiles(null)
      .then((data) => {
        console.log("list data:", data);
        if (cancelled) return;
        setFiles(data)
      })
      .catch((err) => console.error("list failed", err));

    return () => { cancelled = true; };
  }, []);

  console.log({ files });

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3x1 text-ink font-bold">Dashboard</h1>
        <span className="px-4 py-2 rounded bg-tint">Welcome, {user?.username}</span>
      </div>
      <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2">
        {folder.map((f) => (
          <div key={f.id} className="flex flex-col items-center gap-2 p-3 rounded-xl hover:bg-tint/40">
            <Folder className="w-12 h-12 text-accent fill-tint/60" strokeWidth={1.5} />
            <span className="w-full text-sm text-ink text-center truncate" title={f.name}>
              {f.name}
            </span>
          </div>
        ))}
        {files.map((f) => (
          <FileTile key={f.id} file={f} onDownload={handleDownload} onDelete={handleDelete} />
        ))}
      </div>
    </div>
  );
}

