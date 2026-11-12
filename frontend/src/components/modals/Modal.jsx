import { useEffect } from "react";
import { X } from "lucide-react";

export default function Modal({ title, onClose, children }) {
  useEffect(() => {
    const onKey = (e) => e.key === "Escape" && onClose();
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      onClick={onClose}                      // tap outside closes
    >
      <div
        className="relative w-full max-w-md bg-white rounded-2xl p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()} // taps inside don't close
      >
        <button
          onClick={onClose}
          aria-label="Close"
          className="absolute top-3 right-3 p-1.5 rounded-md text-ink/60 hover:bg-tint/40"
        >
          <X className="w-5 h-5" />
        </button>
        {title && <h2 className="text-xl font-bold text-ink mb-4">{title}</h2>}
        {children}
      </div>
    </div>
  );
}
