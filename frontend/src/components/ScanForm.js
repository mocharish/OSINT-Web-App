import React from "react";

export default function ScanForm({ domain, setDomain, loading, onSubmit }) {
  return (
    <form
      onSubmit={onSubmit}
      style={{ display: "flex", justifyContent: "center", marginBottom: "1rem" }}
    >
      <input
        type="text"
        placeholder="Enter domain (e.g. example.com)"
        value={domain}
        onChange={(e) => setDomain(e.target.value)}
        style={{ padding: "10px", width: "300px", fontSize: "1rem" }}
      />
      <button
        type="submit"
        disabled={loading}
        style={{
          padding: "10px 20px",
          marginLeft: "10px",
          fontSize: "1rem",
          cursor: loading ? "not-allowed" : "pointer",
        }}
      >
        {loading ? "Scanning..." : "Run Scan"}
      </button>
    </form>
  );
}
