import { MapPin, Network, Radar } from 'lucide-react'
import { useMemo, useState } from 'react'
import DataTable from './DataTable'

export default function CapacityView({ plan }) {
  const capacity = plan.analytics.capacity
  const [topN, setTopN] = useState(10)
  const [location, setLocation] = useState(capacity.summary[0]?.location_id || '')
  const busiest = capacity.summary.slice(0, topN)
  const maxTotal = Math.max(1, ...busiest.map((item) => item.total_possessions))
  const selected = capacity.locations.find((item) => item.location_id === location)
  const rawRows = useMemo(() => plan.datasets.occupancy.rows.filter((row) => String(row.location_id) === location), [location, plan])
  const locationTotal = capacity.summary.find((item) => item.location_id === location)
  const weeklyMax = Math.max(1, ...(selected?.weeks || []).map((item) => item.possessions))

  return (
    <div className="view-stack">
      <section className="view-title"><div><span className="eyebrow">CAPACITY INTELLIGENCE</span><h2>Network capacity</h2><p>Find pressure points and inspect possession demand by location.</p></div></section>
      <div className="mini-kpis">
        <article><Network size={18} /><span>Locations used</span><strong>{capacity.summary.length}</strong></article>
        <article><MapPin size={18} /><span>Active location-weeks</span><strong>{capacity.locations.reduce((total, item) => total + item.weeks.length, 0)}</strong></article>
        <article><Radar size={18} /><span>Peak weekly possessions</span><strong>{Math.max(0, ...capacity.summary.map((item) => item.peak_weekly_possessions))}</strong></article>
      </div>
      <section className="panel chart-panel">
        <div className="panel-title"><div><h3>Highest-demand locations</h3><p>Ranked by total scheduled possession demand.</p></div><label className="inline-select">Show <select value={topN} onChange={(event) => setTopN(Number(event.target.value))}><option>10</option><option>15</option><option>20</option></select></label></div>
        <div className="bar-chart">
          {busiest.map((item, index) => <div className="bar-row" key={item.location_id}><span className="bar-rank">{String(index + 1).padStart(2, '0')}</span><button onClick={() => setLocation(item.location_id)}>{item.location_id}</button><div className="bar-track"><i style={{ width: `${(item.total_possessions / maxTotal) * 100}%` }} /></div><strong>{item.total_possessions}</strong></div>)}
        </div>
      </section>
      {capacity.summary.length > 0 && <section className="panel inspector-panel">
        <div className="panel-title"><div><h3>Location inspector</h3><p>Weekly demand profile and underlying possession records.</p></div><select value={location} onChange={(event) => setLocation(event.target.value)}>{capacity.summary.map((item) => <option key={item.location_id}>{item.location_id}</option>)}</select></div>
        <div className="location-layout">
          <div className="location-stats"><div><span>Total possessions</span><strong>{locationTotal?.total_possessions || 0}</strong></div><div><span>Activities</span><strong>{locationTotal?.total_activities || 0}</strong></div><div><span>Active weeks</span><strong>{locationTotal?.active_weeks || 0}</strong></div></div>
          <div className="weekly-chart">{selected?.weeks.map((item) => <div key={item.week} title={`Week ${item.week}: ${item.possessions} possessions`}><i style={{ height: `${Math.max(6, (item.possessions / weeklyMax) * 100)}%` }} /><span>{item.week}</span></div>)}</div>
        </div>
        <DataTable dataset={{ columns: plan.datasets.occupancy.columns, rows: rawRows }} />
      </section>}
    </div>
  )
}
