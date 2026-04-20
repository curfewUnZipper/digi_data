export default function StatusBanner({ data }) {
  if (!data) return null;

  const status = data.health;

  const config = {
    Normal: { color: "#22c55e", text: "SYSTEM NORMAL" },
    Degrading: { color: "#facc15", text: "DEGRADING PERFORMANCE" },
    Critical: { color: "#ef4444", text: "CRITICAL CONDITION" }
  };

  const { color, text } = config[status];

  return (
    <div style={{
      background: color,
      padding: 20,
      borderRadius: 12,
      marginBottom: 20,
      textAlign: "center"
    }}>
      <h2>{text}</h2>
      <p>{status}</p>
    </div>
  );
}