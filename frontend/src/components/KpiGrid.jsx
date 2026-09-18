import { Activity, AlertTriangle, CalendarRange, Clock3, TrainFront } from 'lucide-react'

export default function KpiGrid({ summary }) {
  const cards = [
    { label: 'Activities', value: summary.activities, icon: Activity, tone: 'blue' },
    { label: 'Access allocations', value: summary.access_allocations, icon: TrainFront, tone: 'cyan' },
    { label: 'Contracts late', value: summary.contracts_late, icon: AlertTriangle, tone: summary.contracts_late ? 'red' : 'green' },
    { label: 'ECLO accesses', value: summary.eclo_accesses, icon: Clock3, tone: 'amber' },
    { label: 'Final week', value: summary.final_week, icon: CalendarRange, tone: 'violet' },
  ]

  return (
    <div className="kpi-grid">
      {cards.map(({ label, value, icon: Icon, tone }) => (
        <article className="kpi-card" key={label}>
          <div className={`kpi-icon kpi-icon--${tone}`}><Icon size={19} /></div>
          <div><span>{label}</span><strong>{Number(value).toLocaleString()}</strong></div>
          <i className={`kpi-pulse kpi-pulse--${tone}`} />
        </article>
      ))}
    </div>
  )
}
