import { Filter, SearchX } from 'lucide-react'
import { useMemo, useState } from 'react'
import DataTable from './DataTable'

export default function PlanView({ plan }) {
  const rows = plan.datasets.access.rows
  const [activity, setActivity] = useState('all')
  const [accessType, setAccessType] = useState('all')
  const [weekEnd, setWeekEnd] = useState(plan.summary.final_week || 1)

  const filteredRows = useMemo(() => rows.filter((row) => {
    const activityMatch = activity === 'all' || String(row.activity_id) === activity
    const typeMatch = accessType === 'all' || Number(row.eclo) === Number(accessType)
    return activityMatch && typeMatch && Number(row.week) <= weekEnd
  }), [accessType, activity, rows, weekEnd])

  const visibleActivities = [...new Set(filteredRows.map((row) => String(row.activity_id)))]
  const width = Math.max(720, plan.summary.final_week * 26)
  const height = Math.max(260, visibleActivities.length * 32 + 54)

  return (
    <div className="view-stack">
      <section className="panel view-header">
        <div><span className="eyebrow">OPERATIONS BOARD</span><h2>Possession schedule</h2><p>Inspect access allocations across the planning horizon.</p></div>
        <div className="filter-row">
          <label><span>Activity</span><select value={activity} onChange={(event) => setActivity(event.target.value)}><option value="all">All activities</option>{plan.analytics.activity_options.map((item) => <option key={item}>{item}</option>)}</select></label>
          <label><span>Access type</span><select value={accessType} onChange={(event) => setAccessType(event.target.value)}><option value="all">All access</option><option value="0">Standard</option><option value="1">ECLO</option></select></label>
          <label className="range-control"><span>Through week <strong>{weekEnd}</strong></span><input type="range" min="1" max={plan.summary.final_week || 1} value={weekEnd} onChange={(event) => setWeekEnd(Number(event.target.value))} /></label>
        </div>
      </section>

      <section className="panel chart-panel">
        <div className="panel-title"><div><h3>Access timeline</h3><p>{filteredRows.length} allocations · {visibleActivities.length} visible activities</p></div><div className="legend"><span><i className="standard" /> Standard</span><span><i className="eclo" /> ECLO</span></div></div>
        {filteredRows.length ? (
          <div className="timeline-scroll">
            <svg className="timeline" viewBox={`0 0 ${width} ${height}`} style={{ minWidth: width, height }} role="img" aria-label="Possession access timeline">
              {Array.from({ length: weekEnd }, (_, index) => index + 1).map((week) => {
                const x = 150 + ((width - 175) * (week - 1)) / Math.max(1, weekEnd - 1)
                return <g key={week}><line x1={x} y1="30" x2={x} y2={height - 18} className="grid-line" />{(week === 1 || week % Math.ceil(weekEnd / 12) === 0) && <text x={x} y="18" className="axis-label" textAnchor="middle">W{week}</text>}</g>
              })}
              {visibleActivities.map((item, index) => {
                const y = 48 + index * 32
                return <g key={item}><text x="8" y={y + 4} className="activity-label">{item}</text><line x1="150" y1={y} x2={width - 25} y2={y} className="row-line" /></g>
              })}
              {filteredRows.filter((row) => visibleActivities.includes(String(row.activity_id))).map((row, index) => {
                const x = 150 + ((width - 175) * (Number(row.week) - 1)) / Math.max(1, weekEnd - 1)
                const y = 48 + visibleActivities.indexOf(String(row.activity_id)) * 32
                return Number(row.eclo) === 1
                  ? <circle key={index} cx={x} cy={y} r="6" className="mark-eclo"><title>{row.activity_id} · Week {row.week} · {row.access_night}</title></circle>
                  : <rect key={index} x={x - 5} y={y - 5} width="10" height="10" rx="2" transform={`rotate(45 ${x} ${y})`} className="mark-standard"><title>{row.activity_id} · Week {row.week} · {row.access_night}</title></rect>
              })}
            </svg>
          </div>
        ) : <div className="empty-state"><SearchX size={28} /><strong>No allocations match</strong><span>Adjust the current filters to see the schedule.</span></div>}
      </section>

      <section className="panel ledger-panel"><div className="panel-title"><div><h3>Access allocation ledger</h3><p>Detailed scheduler output for the current filters.</p></div><Filter size={18} /></div><DataTable dataset={{ columns: plan.datasets.access.columns, rows: filteredRows }} /></section>
    </div>
  )
}
