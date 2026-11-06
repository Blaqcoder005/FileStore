import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import "./index.css";
import "./output.css";
import { AuthProvider } from "./context/AuthContext";  // Add this import

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>  {/* Add this wrapper */}
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
