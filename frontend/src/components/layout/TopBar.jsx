import { setClientId, getClientId } from '../../api/client'
import Badge from '../ui/Badge'
import { STATUS_COLORS } from '../../utils/labels'

export default function TopBar({ stats, onClientChange, clientId }) {
  const chips = [
    { key: 'PENDING', label: 'Pending', count: stats?.pending ?? 0 },
    { key: 'APPROVED', label: 'Approved', count: stats?.approved ?? 0 },
    { key: 'REJECTED', label: 'Rejected', count: stats?.rejected ?? 0 },
  ]

  return (
    <header className="sticky top-0 z-20 flex h-14 items-center justify-between border-b border-surface-border bg-surface/95 px-6 backdrop-blur">
      <div className="flex items-center gap-3">
        {chips.map(({ key, label, count }) => (
          <div key={key} className="flex items-center gap-2">
            <Badge className={STATUS_COLORS[key]}>{label}</Badge>
            <span className="text-sm font-semibold text-slate-300">{count}</span>
          </div>
        ))}
      </div>
      <div className="flex items-center gap-2">
        <label htmlFor="client" className="text-xs font-medium uppercase tracking-wide text-slate-500">
          Client
        </label>
        <select
          id="client"
          value={clientId}
          onChange={(e) => {
            setClientId(e.target.value)
            onClientChange(e.target.value)
          }}
          className="rounded-lg border border-surface-border bg-surface-overlay px-3 py-1.5 text-sm text-slate-200 focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent"
        >
          <option value="acme">Acme Corp</option>
          <option value="globex">Globex Industries</option>
        </select>
      </div>
    </header>
  )
}
