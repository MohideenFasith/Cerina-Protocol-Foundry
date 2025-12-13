import { useState } from "react";

const API = "http://127.0.0.1:8000";

function App() {
  const [intent, setIntent] = useState("");
  const [project, setProject] = useState<any>(null);

  async function createProject() {
    const res = await fetch(`${API}/api/projects/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ intent }),
    });
    setProject(await res.json());
  }

  async function runWorkflow() {
    await fetch(`${API}/api/projects/${project.project_id}/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ halt_for_human: true }),
    });
    alert("Workflow started — check DB / logs");
  }

  async function approve() {
    await fetch(
      `${API}/api/projects/${project.project_id}/versions/${project.version_id}/approve`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: "Approved from UI" }),
      }
    );
    alert("Approved!");
  }

  return (
    <div style={{ padding: 24 }}>
      <h2>Cerina Protocol Foundry</h2>

      <input
        value={intent}
        onChange={(e) => setIntent(e.target.value)}
        placeholder="Enter CBT intent"
        style={{ width: 420, padding: 8 }}
      />

      <br /><br />

      <button onClick={createProject}>Create Project</button>

      {project && (
        <>
          <p><b>Project ID:</b> {project.project_id}</p>

          <button onClick={runWorkflow}>Run Workflow</button>

          <br /><br />

          <button onClick={approve}>Approve Draft</button>
        </>
      )}
    </div>
  );
}

export default App;
