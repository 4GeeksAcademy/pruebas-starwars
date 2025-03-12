import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

export const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("danger");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const isMounted = useRef(true);

  useEffect(() => {
    return () => {
      isMounted.current = false;
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const response = await fetch("https://reimagined-space-system-x5vpvvjqwrjvfppq-3001.app.github.dev/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      
      const data = await response.json();

      if (response.ok) {
        sessionStorage.setItem("token", data.token);
        if (isMounted.current) {
          setMessage("Inicio de sesión exitoso");
          setMessageType("success");
          window.location.href = "https://reimagined-space-system-x5vpvvjqwrjvfppq-3000.app.github.dev/";
        }
      } else {
        if (isMounted.current) {
          setMessage(data.message || "Error en el inicio de sesión");
          setMessageType("danger");
        }
      }
    } catch (error) {
      if (isMounted.current) {
        setMessage("Error de conexión con el servidor");
        setMessageType("danger");
      }
    } finally {
      if (isMounted.current) {
        setLoading(false);
      }
    }
  };

  return (
    <div className="container mt-5">
      <div className="card shadow p-4">
        <h2 className="text-center mb-4">Iniciar Sesión</h2>
        {message && <div className={`alert alert-${messageType} text-center`}>{message}</div>}
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Correo Electrónico</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="form-control"
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Contraseña</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="form-control"
              required
            />
          </div>
          <button
            type="submit"
            className="btn btn-primary w-100"
            disabled={loading}
          >
            {loading ? "Cargando..." : "Ingresar"}
          </button>
        </form>
      </div>
    </div>
  );
};
