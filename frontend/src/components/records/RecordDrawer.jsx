import { useEffect, useState } from 'react'
import { X, ChevronDown, ChevronRight, Check, Ban } from 'lucide-react'
import { api } from '../../api/client'
import Badge from '../ui/Badge'
import {
  SOURCE_COLORS,
  SOURCE_LABELS,
  STATUS_COLORS,
  SCOPE_COLORS,
  scopeNumber,
  FLAG_LABELS,
  FLAG_STYLES,
} from '../../utils/labels'

function JsonBlock({ data, title, variant }) {
  const [open, setOpen] = useState(true)
  const border = variant === 'raw' ? 'border-emerald-500/30' : 'border-accent/30'
  const headerBg = variant === 'raw' ? 'bg-emerald-500/10' : 'bg-accent/10'

  return (
    <div className={`rounded-lg border ${border} overflow-hidden`}>
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className={`flex w-full items-center justify-between px-3 py-2 text-left text-xs font-semibold uppercase tracking-wide ${headerBg}`}
      >
        {title}
        {open ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
      </button>
      {open && (
        <pre className="max-h-64 overflow-auto bg-black/40 p-3 font-mono text-xs text-slate-300">
          {JSON.stringify(data, null, 2)}
        </pre>
      )}
    </div>
  )
}

function Field({ label, value }) {
  return (
    <div className="rounded-lg border border-surface-border bg-surface/50 px-3 py-2">
      <p className="text-[10px] font-medium uppercase tracking-wider text-slate-500">{label}</p>
      <p className="mt-0.5 text-sm text-slate-200">{value ?? '—'}</p>
    </div>
  )
}

export default function RecordDrawer({ recordId, onClose, onUpdated }) {
  const [record, setRecord] = useState(null)
  const [loading, setLoading] = useState(true)
  const [comment, setComment] = useState('')
  const [acting, setActing] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!recordId) return
    setLoading(true)
    setError(null)
    api
      .record(recordId)
      .then(setRecord)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [recordId])

  const handleApprove = async () => {
    setActing(true)
    try {
      const updated = await api.approve(recordId, {
        reviewed_by: 'analyst',
        notes: comment,
      })
      setRecord(updated)
      onUpdated?.()
    } catch (e) {
      setError(e.message)
    } finally {
      setActing(false)
    }
  }

  const handleReject = async () => {
    setActing(true)
    try {
      const updated = await api.reject(recordId, {
        reviewed_by: 'analyst',
        reason: comment,
      })
      setRecord(updated)
      onUpdated?.()
    } catch (e) {
      setError(e.message)
    } finally {
      setActing(false)
    }
  }

  if (!recordId) return null

  const isPending = record?.status === 'PENDING'

  return (
    <>
      <div
        className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
        aria-hidden
      />
      <aside className="fixed right-0 top-0 z-50 flex h-full w-full max-w-4xl flex-col border-l border-surface-border bg-surface-raised shadow-drawer">
        <div className="flex items-center justify-between border-b border-surface-border px-5 py-4">
          <div>
            <h2 className="text-lg font-semibold text-white">
              Record #{recordId}
            </h2>
            {record && (
              <div className="mt-2 flex flex-wrap gap-2">
                <Badge className={SOURCE_COLORS[record.source_type]}>
                  {SOURCE_LABELS[record.source_type]}
                </Badge>
                <Badge className={STATUS_COLORS[record.status]}>{record.status}</Badge>
                <Badge className={SCOPE_COLORS[record.scope]}>
                  Scope {scopeNumber(record.scope)}
                </Badge>
              </div>
            )}
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-2 text-slate-400 hover:bg-surface-overlay hover:text-white"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-5">
          {loading && <p className="text-slate-500">Loading record…</p>}
          {error && (
            <div className="rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-300">
              {error}
            </div>
          )}
          {record && (
            <>
              <section className="mb-6">
                <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-slate-500">
                  Quality flags
                </h3>
                <div className="flex flex-wrap gap-2">
                  {(record.quality_flags?.length ? record.quality_flags : ['NONE']).map((f) =>
                    f === 'NONE' ? (
                      <span key="none" className="text-sm text-slate-500">No issues flagged</span>
                    ) : (
                      <span
                        key={f}
                        className={`rounded-md border px-2.5 py-1 text-xs font-medium ${FLAG_STYLES[f] || ''}`}
                      >
                        {FLAG_LABELS[f] || f}
                      </span>
                    ),
                  )}
                </div>
              </section>

              <div className="grid gap-4 lg:grid-cols-2">
                <div className="space-y-3">
                  <h3 className="text-xs font-semibold uppercase tracking-wider text-emerald-400/90">
                    Raw data (as ingested)
                  </h3>
                  <JsonBlock
                    title="Source row"
                    data={record.raw_row ?? {}}
                    variant="raw"
                  />
                  <JsonBlock
                    title="Full upload payload"
                    data={record.raw_record?.payload}
                    variant="raw"
                  />
                </div>
                <div className="space-y-3">
                  <h3 className="text-xs font-semibold uppercase tracking-wider text-accent">
                    Normalized emissions
                  </h3>
                  <div className="grid grid-cols-2 gap-2">
                    <Field label="Category" value={record.category} />
                    <Field label="Activity date" value={record.activity_date} />
                    <Field
                      label="Quantity (raw)"
                      value={
                        record.quantity_raw != null
                          ? `${record.quantity_raw} ${record.unit_raw || ''}`
                          : null
                      }
                    />
                    <Field
                      label="Quantity (normalized)"
                      value={
                        record.quantity_normalized != null
                          ? `${record.quantity_normalized} ${record.unit_normalized || ''}`
                          : null
                      }
                    />
                    <Field label="Location" value={record.location} />
                    <Field label="Scope" value={`Scope ${scopeNumber(record.scope)}`} />
                  </div>
                  <Field label="Description" value={record.description} />
                  <JsonBlock
                    title="Normalized payload"
                    data={record.normalized_payload}
                    variant="norm"
                  />
                </div>
              </div>
            </>
          )}
        </div>

        {record && isPending && (
          <div className="sticky bottom-0 border-t border-surface-border bg-surface-raised p-4">
            <label className="mb-2 block text-xs font-medium text-slate-500">
              Review comment (optional)
            </label>
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              rows={2}
              placeholder="Add notes for audit trail…"
              className="mb-3 w-full rounded-lg border border-surface-border bg-surface px-3 py-2 text-sm text-slate-200 placeholder:text-slate-600 focus:border-accent focus:outline-none"
            />
            <div className="flex gap-3">
              <button
                type="button"
                disabled={acting}
                onClick={handleApprove}
                className="flex flex-1 items-center justify-center gap-2 rounded-lg bg-emerald-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-emerald-500 disabled:opacity-50"
              >
                <Check className="h-4 w-4" />
                Approve
              </button>
              <button
                type="button"
                disabled={acting}
                onClick={handleReject}
                className="flex flex-1 items-center justify-center gap-2 rounded-lg bg-red-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-red-500 disabled:opacity-50"
              >
                <Ban className="h-4 w-4" />
                Reject
              </button>
            </div>
          </div>
        )}
        {record && !isPending && record.reviewed_by && (
          <div className="border-t border-surface-border px-5 py-3 text-xs text-slate-500">
            Reviewed by {record.reviewed_by} · {record.reviewed_at}
            {record.review_notes && ` — ${record.review_notes}`}
          </div>
        )}
      </aside>
    </>
  )
}
