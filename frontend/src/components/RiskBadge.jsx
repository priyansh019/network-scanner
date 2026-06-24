export default function RiskBadge({ level }) {
  const normalized = (level || 'low').toLowerCase()
  return (
    <span className={`badge badge-${normalized}`}>
      {normalized}
    </span>
  )
}

export function StatusBadge({ status }) {
  const normalized = (status || 'initiated').toLowerCase()
  return (
    <span className={`badge badge-${normalized}`}>
      {normalized}
    </span>
  )
}
