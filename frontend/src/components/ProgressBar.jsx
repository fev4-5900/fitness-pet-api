const STEPS = 20

export default function ProgressBar({ value, max, color = '#4E7A44' }) {
  const pct = max > 0 ? Math.min(100, Math.round((value / max) * 100)) : 0
  const filled = Math.round((pct / 100) * STEPS)
  return (
    <div className="pbar">
      <div className="pbar-track">
        {Array.from({ length: STEPS }).map((_, i) => (
          <span
            key={i}
            className="pbar-notch"
            style={{ background: i < filled ? color : undefined }}
          />
        ))}
      </div>
      <span className="pbar-num">
        {Math.round(value * 10) / 10}
        {max > 0 ? ` / ${Math.round(max * 10) / 10}` : ''}
      </span>
    </div>
  )
}
