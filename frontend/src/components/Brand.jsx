export default function Brand({ compact = false }) {
  return (
    <div className={`brand ${compact ? 'brand--compact' : ''}`}>
      <div className="brand__mark" aria-hidden="true">
        <span />
        <span />
        <span />
      </div>
      <div>
        <strong>Track Access</strong>
        <small>PLANNING CONTROL</small>
      </div>
    </div>
  )
}
