import { Bell, ChevronDown, Menu, RefreshCw } from 'lucide-react'
import { useState } from 'react'
import AssuranceView from './components/AssuranceView'
import Brand from './components/Brand'
import CapacityView from './components/CapacityView'
import DeliveryView from './components/DeliveryView'
import ExportView from './components/ExportView'
import KpiGrid from './components/KpiGrid'
import PlanSetup from './components/PlanSetup'
import PlanView from './components/PlanView'
import Sidebar from './components/Sidebar'
import { usePlanner } from './hooks/usePlanner'

const TITLES = { plan: 'Possession plan', capacity: 'Network capacity', delivery: 'Contract delivery', assurance: 'Plan assurance', export: 'Schedule export' }

export default function App() {
  const [active, setActive] = useState('plan')
  const [mobileNav, setMobileNav] = useState(false)
  const { plan, loading, error, run, clearError } = usePlanner()

  async function generate(files, scenario) {
    const result = await run(files, scenario)
    if (result) setActive('plan')
  }

  if (!plan) {
    return <div className="launch-shell"><header className="launch-header"><Brand compact /><div className="system-state"><i /> PLANNING SYSTEM ONLINE</div><span className="header-rule" /><div className="agency">LAND TRANSPORT<br /><strong>AUTHORITY</strong></div></header><main><PlanSetup onRun={generate} loading={loading} error={error} onClearError={clearError} /></main><footer><span>TRACK ACCESS CONTROL CENTRE · v2.0</span><span>Railway possession planning & capacity management</span></footer></div>
  }

  const views = { plan: <PlanView plan={plan} />, capacity: <CapacityView plan={plan} />, delivery: <DeliveryView plan={plan} />, assurance: <AssuranceView plan={plan} />, export: <ExportView plan={plan} /> }
  return (
    <div className={`dashboard-shell ${mobileNav ? 'nav-open' : ''}`}>
      <Sidebar active={active} onChange={(key) => { setActive(key); setMobileNav(false) }} plan={plan} />
      <div className="dashboard-main">
        <header className="dashboard-header">
          <button className="mobile-menu" onClick={() => setMobileNav(!mobileNav)} aria-label="Toggle navigation"><Menu size={20} /></button>
          <div><span>LTA NETWORK OPERATIONS</span><strong>{TITLES[active]}</strong></div>
          <div className="dashboard-actions"><span className="live-status"><i /> SYSTEM ONLINE</span><button className="icon-button" aria-label="Notifications"><Bell size={17} /></button><button className="scenario-pill" title="Active strategy">MODE {plan.scenario}<ChevronDown size={14} /></button><button className="rerun-button" onClick={() => window.location.reload()}><RefreshCw size={15} /> New plan</button></div>
        </header>
        <main className="dashboard-content"><div className="plan-heading"><div><span>ACTIVE POSSESSION PLAN</span><h1>{plan.scenario_name}</h1></div><span className="plan-id">PLAN · {new Date().toISOString().slice(0, 10).replaceAll('-', '')}</span></div><KpiGrid summary={plan.summary} />{views[active]}</main>
      </div>
    </div>
  )
}
