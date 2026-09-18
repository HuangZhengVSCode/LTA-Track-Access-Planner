import { BarChart3, CalendarDays, CheckCircle2, Database, Download, PanelLeftClose, Route } from 'lucide-react'
import Brand from './Brand'

const items = [
  ['plan', 'Possession plan', CalendarDays],
  ['capacity', 'Network capacity', BarChart3],
  ['delivery', 'Contract delivery', Route],
  ['assurance', 'Plan assurance', CheckCircle2],
  ['export', 'Schedule export', Download],
]

export default function Sidebar({ active, onChange, plan }) {
  return (
    <aside className="sidebar">
      <Brand />
      <div className="sidebar__label">OPERATIONS</div>
      <nav aria-label="Dashboard sections">
        {items.map(([key, label, Icon]) => (
          <button key={key} className={active === key ? 'active' : ''} onClick={() => onChange(key)} disabled={!plan}>
            <Icon size={18} /><span>{label}</span>
          </button>
        ))}
      </nav>
      <div className="sidebar__network">
        <div className="network-glyph"><Database size={18} /></div>
        <div><strong>{plan ? 'Network loaded' : 'No active plan'}</strong><span>{plan ? `${plan.summary.access_allocations} allocations` : 'Upload source tables'}</span></div>
        <i className={plan ? 'online' : ''} />
      </div>
      <div className="sidebar__footer"><PanelLeftClose size={15} /> LTA · Network Operations</div>
    </aside>
  )
}
