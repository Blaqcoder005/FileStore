import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";
import { FolderOpen } from "lucide-react";

export default function Login() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const { checkAuth } = useAuth(); //talks to the server

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("username", username);
      formData.append("email", email);
      formData.append("password", password);

      const res = await fetch("/api/auth/login", {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      if (res.ok) {
        await checkAuth();          //  sync frontend with backend
        navigate("/dashboard");     //  now ProtectedRoute passes
        return;
      }

      if (res.status === 401) {
        setError("Invalid credentials");
      } else if (res.status === 429) {
        setError("Too many attempts. Try again later.");
      } else {
        const text = await res.text();
        setError(text || "Login failed");
      }
    } catch (err) {
      console.error(err);
      setError("Network error");
    } finally {
      setLoading(false);
    }
  };
return (
  <div className="min-h-screen bg-dark flex items-center justify-center px-4">
    <form
      onSubmit={handleSubmit}
      className="w-full max-w-md bg-white rounded-2xl p-8 shadow-2xl flex flex-col gap-4"
    >
      <div className="flex flex-col items-center gap-2 mb-2">
        <div className="p-3 rounded-2xl bg-tint/50">
          <FolderOpen className="w-8 h-8 text-primary" strokeWidth={1.75} />
        </div>
        <h2 className="text-3xl font-bold text-ink">FileStore</h2>
        <p className="text-sm text-ink/60">Sign in to your files</p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-300 text-red-700 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      <input
        type="text"
        placeholder="Username"
        autoComplete="username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
        className="w-full bg-surface border border-tint rounded-lg px-4 py-3 text-ink placeholder-ink/40
focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/30"
      />

      <input
        type="email"
        placeholder="Email"
        autoComplete="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
        className="w-full bg-surface border border-tint rounded-lg px-4 py-3 text-ink placeholder-ink/40
focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/30"
      />

      <input
        type="password"
        placeholder="Password"
        autoComplete="current-password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
        className="w-full bg-surface border border-tint rounded-lg px-4 py-3 text-ink placeholder-ink/40
focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/30"
      />

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-primary hover:bg-primary-hover text-white font-semibold py-3 rounded-lg transition-colors
disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? "Signing in..." : "Sign in"}
      </button>

      <p className="text-ink/60 text-sm text-center">
        Don't have an account?{" "}
        <Link to="/register" className="text-primary font-medium hover:text-primary-hover">
          Register
        </Link>
      </p>
    </form>
  </div>
 );
}

