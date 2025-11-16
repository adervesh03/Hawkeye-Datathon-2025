import React, { useMemo, useState } from "react";
import "./index.css";

export default function App() {
  const API_URL = useMemo(() => {
    const u = new URL(window.location.href);
    return u.searchParams.get("api") || import.meta.env.VITE_API_URL || "";
  }, []);

  const [form, setForm] = useState({
    veh_value: 6.5,
    veh_body: "SUV",
    veh_age: 3,
    engine_type: "gas",
    max_power: 128,
    veh_color: "silver",
    gender: "M",
    agecat: 2,
    e_bill: 1,
    area: "A",
    time_driven: "12pm - 6pm",
    marital_status: "S",
    low_education_ind: 0,
    credit_score: 650,
    driving_history_score: 85,
    exposure: 0.45
  });

  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");
  const [result, setResult] = useState(null);

  const upd = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  async function onSubmit(e) {
    e.preventDefault();
    setErr("");
    setResult(null);
    if (!API_URL) {
      setErr("API URL not set. Add ?api=https://... or set VITE_API_URL in .env");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${API_URL.replace(/\/$/, "")}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(serialize(form)),
      });
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(`${res.status} ${res.statusText}: ${txt}`);
      }
      setResult(await res.json());
    } catch (e) {
      setErr(e.message || String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="container">
        <header className="header">
          <h1>FutureBright Actuarial Intelligence Risk Assessment</h1>
          <div className="sub">Estimate expected loss and risk segment</div>
        </header>

        <form className="grid" onSubmit={onSubmit}>
          <Card title="Vehicle">
            <Field label="Vehicle Value">
              <input className="input" type="number" step="0.01"
                     value={form.veh_value}
                     onChange={(e)=>upd("veh_value", toNum(e.target.value))}/>
            </Field>
            <Field label="Vehicle Body">
              <select className="input" value={form.veh_body}
                      onChange={(e)=>upd("veh_body", e.target.value)}>
                {["SUV","sedan","hatchback","truck","van","coupe","wagon","other"].map(x=>(
                  <option key={x} value={x}>{x}</option>
                ))}
              </select>
            </Field>
            <Field label="Vehicle Age (years)">
              <input className="input" type="number" value={form.veh_age}
                     onChange={(e)=>upd("veh_age", toInt(e.target.value))}/>
            </Field>
            <Field label="Engine Type">
              <select className="input" value={form.engine_type}
                      onChange={(e)=>upd("engine_type", e.target.value)}>
                {["petrol","diesel","hybrid","electric"].map(x=>(
                  <option key={x} value={x}>{x}</option>
                ))}
              </select>
            </Field>
            <Field label="Max Power (hp)">
              <input className="input" type="number" value={form.max_power}
                     onChange={(e)=>upd("max_power", toNum(e.target.value))}/>
            </Field>
            <Field label="Vehicle Color">
              <select className="input" value={form.veh_color}
                      onChange={(e)=>upd("veh_color", e.target.value)}>
                {["black","blue","brown","gray","green","red","silver","white","yellow"].map(x=> <option key={x} value={x}>{x}</option>)}
              </select>
            </Field>
          </Card>

          <Card title="Policyholder">
            <Field label="Gender">
              <select className="input" value={form.gender}
                      onChange={(e)=>upd("gender", e.target.value)}>
                {["M","F","O"].map(x=> <option key={x} value={x}>{x}</option>)}
              </select>
            </Field>
            <Field label="Age Category">
              <input className="input" type="number" value={form.agecat}
                     onChange={(e)=>upd("agecat", toInt(e.target.value))}/>
            </Field>
            <Field label="E-bill Enabled">
              <select className="input" value={form.e_bill}
                      onChange={(e)=>upd("e_bill", toInt(e.target.value))}>
                <option value={1}>Yes</option>
                <option value={0}>No</option>
              </select>
            </Field>
            <Field label="Marital Status">
              <select className="input" value={form.marital_status}
                      onChange={(e)=>upd("marital_status", e.target.value)}>
                {["S","M","D","W"].map(x=> <option key={x} value={x}>{x}</option>)}
              </select>
            </Field>
            <Field label="Low Education Indicator">
              <select className="input" value={form.low_education_ind}
                      onChange={(e)=>upd("low_education_ind", toInt(e.target.value))}>
                <option value={0}>No</option>
                <option value={1}>Yes</option>
              </select>
            </Field>
            <Field label="Credit Score">
              <input className="input" type="number" value={form.credit_score}
                     onChange={(e)=>upd("credit_score", toNum(e.target.value))}/>
            </Field>
            <Field label="Driving History Score">
              <input className="input" type="number" value={form.driving_history_score}
                     onChange={(e)=>upd("driving_history_score", toNum(e.target.value))}/>
            </Field>
            <Field label="Exposure">
              <input className="input" type="number" value={form.exposure}
                     onChange={(e)=>upd("exposure", toNum(e.target.value))}/>
            </Field>
          </Card>

          <Card title="Driving Behavior">
            <Field label="Area">
              <select className="input" value={form.area}
                      onChange={(e)=>upd("area", e.target.value)}>
                {["A","B","C","D","Urban","Suburban","Rural"].map(x=>(
                  <option key={x} value={x}>{x}</option>
                ))}
              </select>
            </Field>
            <Field label="Time Driven">
              <select className="input" value={form.time_driven}
                      onChange={(e)=>upd("time_driven", e.target.value)}>
                {["12am - 6am","6am - 12pm","12pm - 6pm","6pm - 12am"].map(x=>(
                  <option key={x} value={x}>{x}</option>
                ))}
              </select>
            </Field>
          </Card>

          <div className="actions">
            <button className="button" type="submit" disabled={loading}>
              {loading ? "Loading..." : "Calculate"}
            </button>
            {err && <div className="error">{err}</div>}
          </div>
        </form>

        {result && (
          <div className="results">
            <div className="stat">
              <div className="stat-label">Predicted Total Loss</div>
              <div className="stat-value">
                {fmtUSD(result.pred_total_loss)}
              </div>
            </div>

            <div className="stat">
              <div className="stat-label">Predicted Loss per Exposure</div>
              <div className="stat-value">
                {fmtUSD(result.pred_per_exposure)}
              </div>
            </div>

            <div className="stat">
              <div className="stat-label">Calibrated Loss per Exposure</div>
              <div className="stat-value">
                {fmtUSD(result.pred_per_exposure_rescale)}
              </div>
            </div>

            {"risk_segment_kmeans" in result && (
              <div className="stat">
                <div className="stat-label">Risk Segment (K-Means)</div>
                <div className="stat-value">{result.risk_segment_kmeans}</div>
              </div>
            )}

            {"risk_segment_quantile" in result && (
              <div className="stat">
                <div className="stat-label">Risk Segment (Quantile)</div>
                <div className="stat-value">{result.risk_segment_quantile}</div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function Card({ title, children }) {
  return (
    <div className="card">
      <div className="card-title">{title}</div>
      <div className="card-grid">{children}</div>
    </div>
  );
}

function Field({ label, children }) {
  return (
    <label className="field">
      <div className="field-label">{label}</div>
      {children}
    </label>
  );
}

const toNum = (v) => (v === "" ? null : Number(v));
const toInt = (v) => (v === "" ? null : parseInt(v));

function fmtUSD(x) {
  if (x == null || isNaN(x)) return "—";
  try { return new Intl.NumberFormat(undefined, { style: "currency", currency: "USD" }).format(x); }
  catch { return String(x); }
}

function serialize(f) {
  return {
    veh_value: toNum(f.veh_value),
    veh_body: f.veh_body,
    veh_age: toInt(f.veh_age),
    engine_type: f.engine_type,
    max_power: toNum(f.max_power),
    veh_color: f.veh_color,
    gender: f.gender,
    agecat: toInt(f.agecat),
    e_bill: toInt(f.e_bill),
    area: f.area,
    time_driven: f.time_driven,
    marital_status: f.marital_status,
    low_education_ind: toInt(f.low_education_ind),
    credit_score: toNum(f.credit_score),
    driving_history_score: toNum(f.driving_history_score),
    exposure: toNum(f.exposure),
  };
}