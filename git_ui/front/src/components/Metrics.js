export default function Metrics({ data }) {
  if (!data) return null;

  const cards = [
    { label: "CPU Temp", value: data.cpu_temp, unit: "°C" },
    { label: "Fan Speed", value: data.fan1, unit: "%" },
    { label: "Predicted Fan", value: data.predicted_fan, unit: "%" },
    { label: "Fan Error", value: data.fan_error, unit: "" }
  ];

  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "repeat(4, 1fr)",
      gap: 20,
      marginBottom: 20
    }}>
      {cards.map((c, i) => (
        <div key={i} style={{
          background: "#1e293b",
          padding: 20,
          borderRadius: 12
        }}>
          <p style={{ color: "#94a3b8" }}>{c.label}</p>
          <h2>{c.value?.toFixed(2)} {c.unit}</h2>
        </div>
      ))}
    </div>
  );
}