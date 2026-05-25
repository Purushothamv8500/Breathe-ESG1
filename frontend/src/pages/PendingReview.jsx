import { useCallback, useEffect, useState } from 'react'
import { useOutletContext } from 'react-router-dom'
import { AlertTriangle, Eye, Check, Ban } from 'lucide-react'
import { api, unwrapRecords } from '../api/client'
import Badge from '../components/ui/Badge'
import RecordDrawer from '../components/records/RecordDrawer'
import {
  SOURCE_COLORS,
  SOURCE_LABELS,
  FLAG_LABELS,
  FLAG_STYLES,
  scopeNumber,
  SCOPE_COLORS,
} from '../utils/labels'

export default function PendingReview() {
  const { refreshStats } = useOutletContext() || {}
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedId, setSelectedId] = useState(null)
  const [actingId, setActingId] = useState(null)

  const load = useCallback(() => {
    setLoading(true)
    api
      .records({ status: 'PENDING' })
      .then((data) => setItems(unwrapRecords(data)))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    load()
  }, [load])

  const quickAction = async (id, action) => {
    setActingId(id)
    try {
      if (action === 'approve') {
        await api.approve(id, { reviewed_by: 'analyst', notes: 'Quick approve from queue' })
      } else {
        await api.reject(id, { reviewed_by: 'analyst', reason: 'Quick reject from queue' })
      }
      load()
      refreshStats?.()
    } finally {
      setActingId(null)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Pending Reviews</h1>
        <p className="mt-1 text-sm text-slate-500">
          Work queue — triage flagged records and approve or reject in bulk workflow
        </p>
      </div>

      {loading && <p className="text-slate-500">Loading queue…</p>}

      {!loading && items.length === 0 && (
        <div className="rounded-xl border border-surface-border bg-surface-raised py-16 text-center">
          <Check className="mx-auto h-10 w-10 text-emerald-500/60" />
          <p className="mt-3 font-medium text-slate-300">Queue clear</p>
          <p className="text-sm text-slate-500">No pending records for this client</p>
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {items.map((r) => (
          <article
            key={r.id}
            className="flex flex-col rounded-xl border border-surface-border bg-surface-raised p-5 shadow-card transition-shadow hover:shadow-lg hover:shadow-black/20"
          >
            <div className="flex items-start justify-between gap-2">
              <Badge className={SOURCE_COLORS[r.source_type]}>
                {SOURCE_LABELS[r.source_type]}
              </Badge>
              <span className={`rounded-full px-2 py-0.5 text-xs font-semibold ${SCOPE_COLORS[r.scope]}`}>
                Scope {scopeNumber(r.scope)}
              </span>
            </div>

            <p className="mt-3 line-clamp-2 text-sm font-medium text-slate-200">
              {r.description || `Record #${r.id}`}
            </p>
            <p className="mt-1 font-mono text-xs text-slate-500">
              {r.quantity_normalized != null
                ? `${r.quantity_normalized} ${r.unit_normalized || ''}`
                : 'Quantity pending'}
              {r.activity_date && ` · ${r.activity_date}`}
            </p>

            <div className="mt-3 flex flex-wrap gap-1.5">
              {(r.quality_flags || []).map((f) => (
                <span
                  key={f}
                  className={`inline-flex items-center gap-1 rounded border px-2 py-0.5 text-[10px] font-medium ${FLAG_STYLES[f]}`}
                >
                  <AlertTriangle className="h-3 w-3" />
                  {FLAG_LABELS[f] || f}
                </span>
              ))}
              {!r.quality_flags?.length && (
                <span className="text-xs text-slate-600">No flags</span>
              )}
            </div>

            <div className="mt-4 flex flex-wrap gap-2 border-t border-surface-border pt-4">
              <button
                type="button"
                onClick={() => setSelectedId(r.id)}
                className="flex items-center gap-1.5 rounded-lg border border-surface-border px-3 py-1.5 text-xs font-medium text-slate-300 hover:bg-surface-overlay"
              >
                <Eye className="h-3.5 w-3.5" />
                View details
              </button>
              <button
                type="button"
                disabled={actingId === r.id}
                onClick={() => quickAction(r.id, 'approve')}
                className="flex items-center gap-1.5 rounded-lg bg-emerald-600/90 px-3 py-1.5 text-xs font-semibold text-white hover:bg-emerald-500 disabled:opacity-50"
              >
                <Check className="h-3.5 w-3.5" />
                Approve
              </button>
              <button
                type="button"
                disabled={actingId === r.id}
                onClick={() => quickAction(r.id, 'reject')}
                className="flex items-center gap-1.5 rounded-lg bg-red-600/90 px-3 py-1.5 text-xs font-semibold text-white hover:bg-red-500 disabled:opacity-50"
              >
                <Ban className="h-3.5 w-3.5" />
                Reject
              </button>
            </div>
          </article>
        ))}
      </div>

      <RecordDrawer
        recordId={selectedId}
        onClose={() => setSelectedId(null)}
        onUpdated={() => {
          load()
          refreshStats?.()
          setSelectedId(null)
        }}
      />
    </div>
  )
}
