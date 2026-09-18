import { CalendarCheck2, CircleAlert, TimerReset } from 'lucide-react'
import DataTable from './DataTable'

export default function DeliveryView({ plan }) {
  const results = [...plan.datasets.results.rows].sort((a, b) => Number(b.overrun_days) - Number(a.overrun_days))
  const maxOverrun = Math.max(1, ...results.map((item) => Number(item.overrun_days)))

  return (
    <div className="view-stack">
      <section className="view-title"><div><span className="eyebrow">DELIVERY CONTROL</span><h2>Contract completion</h2><p>Track programme performance against committed completion dates.</p></div></section>
      <div className="mini-kpis">
        <article><CalendarCheck2 size={18} /><span>Contracts</span><strong>{results.length}</strong></article>
        <article className={plan.summary.contracts_late ? 'danger' : 'success'}><CircleAlert size={18} /><span>Contracts late</span><strong>{plan.summary.contracts_late}</strong></article>
        <article className={plan.summary.total_overrun_days ? 'danger' : 'success'}><TimerReset size={18} /><span>Total overrun days</span><strong>{plan.summary.total_overrun_days}</strong></article>
      </div>
      <section className="panel chart-panel">
        <div className="panel-title"><div><h3>Contract schedule overrun</h3><p>Days beyond planned completion by contract.</p></div><span className={`status-chip ${plan.summary.contracts_late ? 'warning' : 'good'}`}>{plan.summary.contracts_late ? 'ATTENTION REQUIRED' : 'ON PROGRAMME'}</span></div>
        <div className="contract-chart">
          {results.map((item) => <div key={item.contract_number}><div className="contract-bar-area"><i style={{ height: `${Number(item.overrun_days) ? Math.max(8, (Number(item.overrun_days) / maxOverrun) * 100) : 3}%` }} className={Number(item.overrun_days) ? 'late' : ''} /><strong>{item.overrun_days}</strong></div><span title={item.contract_number}>{item.contract_number}</span></div>)}
        </div>
      </section>
      <section className="panel ledger-panel"><div className="panel-title"><div><h3>Contract delivery ledger</h3><p>Simulated completion and overrun by contract.</p></div></div><DataTable dataset={{ columns: plan.datasets.results.columns, rows: results }} /></section>
    </div>
  )
}
