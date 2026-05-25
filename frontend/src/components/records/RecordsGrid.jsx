import { AlertTriangle } from 'lucide-react'
import Badge from '../ui/Badge'
import {
  SOURCE_COLORS,
  SOURCE_LABELS,
  STATUS_COLORS,
  SCOPE_COLORS,
  scopeNumber,
} from '../../utils/labels'

export default function RecordsGrid({ records, onRowClick, selectedId }) {
  if (!records.length) {
    return (
      <div className="rounded-xl border border-surface-border bg-surface-raised py-16 text-center text-slate-500">
        No records match your filters.
      </div>
    )
  }

  return (
    <div className="overflow-hidden rounded-xl border border-surface-border bg-surface-raised shadow-card">
      <div className="grid grid-cols-[minmax(0,1fr)_repeat(7,minmax(0,auto))] gap-px border-b border-surface-border bg-surface-border text-xs font-semibold uppercase tracking-wider text-slate-500">
        <div className="bg-surface-raised px-4 py-3">Description</div>
        <div className="bg-surface-raised px-4 py-3">Source</div>
        <div className="bg-surface-raised px-4 py-3">Scope</div>
        <div className="bg-surface-raised px-4 py-3 text-right">Quantity</div>
        <div className="bg-surface-raised px-4 py-3">Unit</div>
        <div className="bg-surface-raised px-4 py-3">Status</div>
        <div className="bg-surface-raised px-4 py-3">Date</div>
        <div className="bg-surface-raised px-4 py-3 text-center">Flags</div>
      </div>
      {records.map((r) => (
        <button
          key={r.id}
          type="button"
          onClick={() => onRowClick(r.id)}
          className={`grid w-full grid-cols-[minmax(0,1fr)_repeat(7,minmax(0,auto))] gap-px text-left text-sm transition-colors hover:bg-accent/5 ${
            selectedId === r.id ? 'bg-accent/10' : 'bg-surface-raised'
          }`}
        >
          <div className="truncate px-4 py-3.5 font-medium text-slate-200">
            {r.description || `Record #${r.id}`}
          </div>
          <div className="flex items-center px-4 py-3.5">
            <Badge className={SOURCE_COLORS[r.source_type]}>{SOURCE_LABELS[r.source_type]}</Badge>
          </div>
          <div className="flex items-center px-4 py-3.5">
            <span className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${SCOPE_COLORS[r.scope]}`}>
              {scopeNumber(r.scope)}
            </span>
          </div>
          <div className="px-4 py-3.5 text-right font-mono text-slate-300">
            {r.quantity_normalized ?? '—'}
          </div>
          <div className="px-4 py-3.5 text-slate-400">{r.unit_normalized || '—'}</div>
          <div className="flex items-center px-4 py-3.5">
            <Badge className={STATUS_COLORS[r.status]}>{r.status}</Badge>
          </div>
          <div className="px-4 py-3.5 text-slate-400">{r.activity_date || '—'}</div>
          <div className="flex items-center justify-center px-4 py-3.5">
            {(r.quality_flags?.length ?? 0) > 0 ? (
              <AlertTriangle className="h-4 w-4 text-amber-400" title={r.quality_flags.join(', ')} />
            ) : (
              <span className="text-slate-600">—</span>
            )}
          </div>
        </button>
      ))}
    </div>
  )
}
