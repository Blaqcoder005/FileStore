import {
  File as FileIcon, FileText, Image as ImageIcon, Film, Music, Archive,
  Download, Trash2,
} from "lucide-react";


function iconFor(mime = "") {
  if (mime.startsWith("image/")) return ImageIcon;
  if (mime.startsWith("video/")) return Film;
  if (mime.startsWith("audio/")) return Music;
  if (mime === "application/pdf" || mime.startsWith("text/")) return FileText;
  if (mime.includes("zip") || mime.includes("compressed")) return Archive;
  return FileIcon;
}


export default function FileTile({ file, onDownload, onDelete }) {
  const Icon = iconFor(file.mime_type);

  return (
    <div className="relative group flex flex-col items-center gap-2 p-3 rounded-xl hover:bg-tint/40">
      <Icon className="w-12 h-12 text-primary" strokeWidth={1.5} />
      <span className="w-full text-sm text-ink text-center truncate" title={file.name}>
        {file.name}
      </span>

      <div className="absolute top-1 right-1 flex gap-1 md:opacity-0 md:group-hover:opacity-100 transition">
        <button onClick={() => onDownload(file)} aria-label="Download"
          className="p-1.5 rounded-md bg-white shadow text-primary hover:bg-tint">
          <Download className="w-4 h-4" />
        </button>
        <button onClick={() => onDelete(file)} aria-label="Delete"
          className="p-1.5 rounded-md bg-white shadow text-red-600 hover:bg-red-50">
          <Trash2 className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
