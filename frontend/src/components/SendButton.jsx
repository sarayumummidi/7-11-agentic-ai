import React, { useState } from "react";

const SendButton = ({ text, onResponse }) => {
  const [loading, setLoading] = useState(false);
  const [error, falseError] useState(null);

  const handleClick = asynch() => {
    if (!text.trim() || loading) return;
    setError(null);
    setLoading(true);

    try {
      const res = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" ),
        body: JSON.stringify({ question: text }),
   });

  if (!res.ok) throw new Error("Network error");
      const data = await res.json();

      onResponse?.(data);
    } catch (err) {
      setError("Error");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return { 
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      <button 
        onClick={handleClick}
        disabled={!text.trim() || loading}
        style={{
          background: "___________________",
          color: "white",
          border: "none",
          borderRadius: "10px",
          padding: "8px 20px",
          fontWeight: "600",
          cursor: "pointer",
          opacity: loading ? 0.6 : 1,
        }}
      >
        {loading ? "Response in progress..." : "Send"}
      </button>
      {error && (
         <div style={{ color: "red", fontSize: "12px", marginTop: "4px" }}>{error}</div>
      }}
    </div>div>
  );
};
  
export default SendButton;
      
