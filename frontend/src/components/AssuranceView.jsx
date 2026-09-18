import { CheckCircle2, CircleX, FileCheck2, ShieldCheck } from 'lucide-react'

export default function AssuranceView({ plan }) {
  const passed = plan.assurance.filter((check) => check.status === 'pass').length
  return (
    <div className="view-stack">
      <section className="view-title"><div><span className="eyebrow">AUTOMATED ASSURANCE</span><h2>Plan assurance</h2><p>Operational checks applied to the generated possession schedule.</p></div><span className={`assurance-score ${passed === plan.assurance.length ? 'good' : 'warning'}`}><strong>{passed}/{plan.assurance.length}</strong> CHECKS PASSED</span></section>
      <section className="assurance-grid">
        {plan.assurance.map((check, index) => <article className={`assurance-card ${check.status}`} key={check.key}><span className="check-index">0{index + 1}</span><div className="check-icon">{check.status === 'pass' ? <CheckCircle2 size={25} /> : <CircleX size={25} />}</div><small>{check.status === 'pass' ? 'PASSED' : 'REVIEW'}</small><h3>{check.label}</h3><p>{check.message}</p></article>)}
      </section>
      <section className="panel assurance-summary"><ShieldCheck size={29} /><div><span>ASSURANCE OUTCOME</span><h3>{passed === plan.assurance.length ? 'Plan ready for operational review' : 'Intervention required before release'}</h3><p>{passed === plan.assurance.length ? 'All automated controls have passed. Export files are available for downstream review.' : 'Resolve the flagged controls, then regenerate the possession plan.'}</p></div><FileCheck2 size={42} /></section>
    </div>
  )
}
