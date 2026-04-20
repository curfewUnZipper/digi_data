import React, { useState } from "react";
import Tabs from "./components/Tabs";
import Dashboard from "./components/Dashboard";
import InputPanel from "./components/InputPanel";
import DataTable from "./components/DataTable";

function App() {
  const [data, setData] = useState([]);

  return (
    <div style={{
      background: "#0f172a",
      minHeight: "100vh",
      color: "white",
      padding: 20
    }}>
      <h1>🌀 Fan Health Monitor</h1>

      <Tabs
        tabs={[
          { name: "Dashboard", component: <Dashboard data={data} /> },
          { name: "Inputs", component: <InputPanel data={data} setData={setData} /> },
          { name: "Logs", component: <DataTable data={data} /> }
        ]}
      />
    </div>
  );
}

export default App;