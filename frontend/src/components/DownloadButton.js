function DownloadButton({ domain }) {
  if (!domain) return null;

  return (
    <div style={{ textAlign: "center", marginTop: "2rem" }}>
      <button
        style={{
          padding: "10px 20px",
          background: "#4caf50",
          color: "white",
          border: "none",
          cursor: "pointer",
          fontSize: "1rem",
          borderRadius: 4,
        }}
        onClick={() => {
          window.open(`http://localhost:8000/export/${domain}`, "_blank");
        }}
      >
        Download Excel Report
      </button>
    </div>
  );
}

export default DownloadButton;
