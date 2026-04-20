import React, { useEffect, useState } from "react";
import { getRULSeries } from "../api";

export default function RULPanel({ data }) {
  const [rul, setRul] = useState(null);

  useEffect(() => {
    async function fetchRUL() {
      const res = await getRULSeries(data);
      setRul(res);
    }
    fetchRUL();
  }, [data]);

  if (!rul) return <p>Need at least 50 rows</p>;

  const latest = rul.filter(r => r !== null).slice(-1)[0];

  return (
    <div>
      <h2>RUL</h2>
      <p>Years: {latest?.years.toFixed(2)}</p>
      <p>Hours: {latest?.hours.toFixed(0)}</p>

      {latest?.years > 5 && <p>✅ Healthy</p>}
      {latest?.years <= 5 && latest?.years > 2 && <p>⚠️ Moderate</p>}
      {latest?.years <= 2 && <p>🚨 Critical</p>}
    </div>
  );
}