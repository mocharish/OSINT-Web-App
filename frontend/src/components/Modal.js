import React from "react";

export default function Modal({ data, onClose }) {
  return (
    <div
      style={{
        position: "fixed", top: 0, left: 0, right: 0, bottom: 0,
        background: "rgba(0,0,0,0.5)",
        display: "flex", justifyContent: "center", alignItems: "center",
      }}
    >
      <div
        style={{
          background: "white",
          padding: "2rem",
          maxWidth: 700,
          overflowY: "auto",
          maxHeight: "90vh",
        }}
      >
        <h3>Details for {data.domain}</h3>
        <pre style={{ whiteSpace: "pre-wrap", fontSize: "0.85rem" }}>
          {JSON.stringify(data, null, 2)}
        </pre>
        <button onClick={onClose} style={{ marginTop: "1rem" }}>Close</button>
      </div>
    </div>
  );
}
