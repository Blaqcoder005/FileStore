import { useState } from "react";
import { useNavigate } from "react-router-dom";
// import "../styles/login.css";
import { useAuth } from "../context/AuthContext";

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
  <div className="min-h-screen bg-slate-900 flex items-center justify-center px-4">
    <form
      onSubmit={handleSubmit}
      className="w-full max-w-md bg-slate-800 rounded-2xl p-8 shadow-2xl flex flex-col gap-4"
    >
      <h2 className="text-3xl font-bold text-white text-center">Sign-in</h2>

      {error && (
        <div className="bg-red-500/20 border border-red-500 text-red-400 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
        className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-3 text-white placeholder-slate-400
focus:outline-none focus:border-teal-500"
      />

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
        className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-3 text-white placeholder-slate-400
focus:outline-none focus:border-teal-500"
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
        className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-3 text-white placeholder-slate-400
focus:outline-none focus:border-teal-500"
      />

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-teal-600 hover:bg-teal-700 text-white font-semibold py-3 rounded-lg transition-colors
disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? "Signing in" : "sign-in"}
      </button>

      <p className="text-slate-400 text-sm text-center">
        Already have an account?{" "}
        <a href="/login" className="text-teal-400 hover:text-teal-300">
          Login
        </a>
      </p>
    </form>
  </div>
 );
}
