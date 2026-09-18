import { Download, FileDown, Table2 } from 'lucide-react'
import { useState } from 'react'
import { downloadDataset } from '../lib/csv'
import DataTable from './DataTable'

const OUTPUTS = [
  ['access', 'SCHEDULE_ACCESS.csv', 'Access allocation sequence and week'],
  ['occupancy', 'SCHEDULE_OCCUPANCY.csv', 'Location occupancy and sharing groups'],
  ['results', 'RESULTS.csv', 'Contract completion performance'],
]

export default function ExportView({ plan }) {
  const [preview, setPreview] = useState('access')
  return (
    <div className="view-stack">
      <section className="view-title"><div><span className="eyebrow">OUTPUT PACKAGE</span><h2>Schedule export</h2><p>Download the generated operational datasets.</p></div><span className="status-chip good">READY TO EXPORT</span></section>
      <section className="export-grid">
        {OUTPUTS.map(([key, filename, description], index) => <article key={key}><div className="export-icon"><FileDown size={21} /></div><small>OUTPUT 0{index + 1}</small><h3>{filename}</h3><p>{description}</p><div><span>{plan.datasets[key].rows.length.toLocaleString()} rows</span><button onClick={() => downloadDataset(plan.datasets[key], filename)}><Download size={16} /> Download</button></div></article>)}
      </section>
      <section className="panel ledger-panel"><div className="panel-title"><div><h3>Output preview</h3><p>Inspect each dataset before download.</p></div><div className="segmented">{OUTPUTS.map(([key]) => <button className={preview === key ? 'active' : ''} onClick={() => setPreview(key)} key={key}><Table2 size={14} /> {key}</button>)}</div></div><DataTable dataset={plan.datasets[preview]} /></section>
    </div>
  )
}
