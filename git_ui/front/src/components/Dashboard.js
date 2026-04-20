import Gauge from "./Gauge";
import StatusBanner from "./StatusBanner";
import Metrics from "./Metrics";
import Charts from "./Charts";

export default function Dashboard({ data }) {
  const latest = data[data.length - 1];

  if (!latest) return <p>No data yet</p>;

  return (
    <div>

      <StatusBanner data={latest} />

      {/* 🔥 MAIN SECTION */}
      <div style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: 30
      }}>
        <div>
          <h3>Anomaly Score</h3>
          <Gauge value={latest.anomaly_score} />
          {/* 🔥 ANOMALY BAR */}
            <div style={{
            marginTop: 10,
            height: 10,
            background: "#1e293b",
            borderRadius: 5,
            overflow: "hidden",
            width: 200
            }}>
            <div style={{
                width: `${latest.anomaly_score}%`,
                background:
                latest.anomaly_score < 35 ? "#22c55e" :
                latest.anomaly_score < 70 ? "#facc15" :
                "#ef4444",
                height: "100%"
            }} />
            </div>
        </div>

        <div style={{ flex: 1, marginLeft: 40 }}>
          <Metrics data={latest} />
        </div>
      </div>

      <Charts data={data} />

    </div>
  );
}