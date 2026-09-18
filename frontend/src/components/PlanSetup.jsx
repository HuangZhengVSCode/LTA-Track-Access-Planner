import { AlertCircle, ArrowRight, Check, FileSpreadsheet, Layers3, LoaderCircle, UploadCloud, X } from 'lucide-react'
import { useMemo, useRef, useState } from 'react'

export const REQUIRED_TABLES = [
  '01_LINES', '02_STATIONS', '03_SECTORS', '04_LOCATION_SUPPLY',
  '05_BUFFER_LOCATION', '06_PARAMETERS', '07_PROJECT_DETAILS', '08_ACTIVITY_DETAILS',
]

const SCENARIOS = {
  A: { index: '01', title: 'Fixed Capacity', caption: 'Capacity first', description: 'Protect the nominal network envelope. The programme may extend to absorb demand.', accent: 'blue' },
  B: { index: '02', title: 'Fixed Completion Dates', caption: 'Delivery first', description: 'Hold committed dates using controlled excess capacity and ECLO access.', accent: 'amber' },
  C: { index: '03', title: 'Balanced Operations', caption: 'Optimised balance', description: 'Trade capacity pressure against delivery dates with continuity controls.', accent: 'green' },
}

function matches(file, table) {
  return file.name.toUpperCase().includes(table)
}

export default function PlanSetup({ onRun, loading, error, onClearError }) {
  const [scenario, setScenario] = useState('A')
  const [files, setFiles] = useState([])
  const [dragging, setDragging] = useState(false)
  const inputRef = useRef(null)

  const readiness = useMemo(() => REQUIRED_TABLES.map((table) => ({ table, file: files.find((file) => matches(file, table)) })), [files])
  const ready = files.length === 8 && readiness.every((entry) => entry.file)

  function accept(nextFiles) {
    onClearError()
    const csvFiles = Array.from(nextFiles).filter((file) => file.name.toLowerCase().endsWith('.csv'))
    setFiles((currentFiles) => {
      const byName = new Map(currentFiles.map((file) => [file.name.toLowerCase(), file]))
      for (const file of csvFiles) byName.set(file.name.toLowerCase(), file)
      return [...byName.values()].slice(0, 8)
    })
  }

  return (
    <div className="setup-page">
      <section className="setup-intro">
        <span className="eyebrow"><i /> CONTROL CENTRE · PLAN GENERATION</span>
        <h1>Build a possession plan<br /><em>with operational clarity.</em></h1>
        <p>Load your network instance, select an operating strategy, and generate a plan with capacity and delivery assurance built in.</p>
        <div className="route-line" aria-hidden="true"><span /><i /><i /><i /><span /></div>
      </section>

      <div className="setup-grid">
        <section className="panel scenario-panel">
          <div className="section-heading"><span>01</span><div><h2>Operating strategy</h2><p>Choose how the scheduler resolves competing priorities.</p></div></div>
          <div className="scenario-list">
            {Object.entries(SCENARIOS).map(([key, item]) => (
              <button key={key} className={`scenario-card scenario-card--${item.accent} ${scenario === key ? 'selected' : ''}`} onClick={() => setScenario(key)}>
                <span className="scenario-card__index">{item.index}</span>
                <div><small>{item.caption}</small><strong>{item.title}</strong><p>{item.description}</p></div>
                <span className="radio-mark">{scenario === key && <Check size={13} />}</span>
              </button>
            ))}
          </div>
        </section>

        <section className="panel upload-panel">
          <div className="section-heading"><span>02</span><div><h2>Network instance</h2><p>All eight source tables are required.</p></div></div>
          <button
            className={`dropzone ${dragging ? 'dragging' : ''}`}
            onClick={() => inputRef.current?.click()}
            onDragOver={(event) => { event.preventDefault(); setDragging(true) }}
            onDragLeave={() => setDragging(false)}
            onDrop={(event) => { event.preventDefault(); setDragging(false); accept(event.dataTransfer.files) }}
          >
            <input
              ref={inputRef}
              type="file"
              accept=".csv,text/csv"
              multiple
              hidden
              onChange={(event) => {
                accept(event.target.files)
                event.target.value = ''
              }}
            />
            <span className="dropzone__icon"><UploadCloud size={25} /></span>
            <strong>Drop CSV tables here</strong>
            <span>select all eight together or add them one at a time · 25 MB max per file</span>
          </button>
          <div className="file-status-head"><span>Source table manifest</span><strong className={ready ? 'complete' : ''}>{readiness.filter((entry) => entry.file).length} / 8</strong></div>
          <div className="file-manifest">
            {readiness.map(({ table, file }) => (
              <div key={table} className={file ? 'loaded' : ''}>
                {file ? <Check size={13} /> : <FileSpreadsheet size={13} />}
                <span>{table.replace(/^\d\d_/, '').replaceAll('_', ' ')}</span>
                <small>{file ? 'READY' : 'MISSING'}</small>
              </div>
            ))}
          </div>
          {files.length > 0 && !ready && (
            <button className="clear-files" onClick={() => setFiles([])}><X size={14} /> Clear selection</button>
          )}
        </section>
      </div>

      {error && <div className="error-banner"><AlertCircle size={18} /><span>{error}</span></div>}

      <section className="run-strip">
        <div className="run-strip__state"><Layers3 size={19} /><div><span>PLANNING ENGINE</span><strong>{ready ? 'Network package verified' : 'Awaiting complete network package'}</strong></div></div>
        <div className="run-strip__track"><i className={ready ? 'active' : ''} /><span /><span /><span /></div>
        <button className="primary-button" disabled={!ready || loading} onClick={() => onRun(files, scenario)}>
          {loading ? <><LoaderCircle className="spin" size={18} /> Generating plan</> : <>Generate possession plan <ArrowRight size={18} /></>}
        </button>
      </section>
    </div>
  )
}
