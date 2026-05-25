export default function KpiCard({ title, value, icon: Icon, gradientClass, accentClass }) {
  return (
    <div
      className={`relative overflow-hidden rounded-xl border border-surface-border bg-surface-raised p-5 shadow-card ${gradientClass}`}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-slate-500">{title}</p>
          <p className="mt-2 text-3xl font-bold tracking-tight text-white">{value ?? '—'}</p>
        </div>
        <div className={`rounded-lg p-2.5 ${accentClass}`}>
          <Icon className="h-5 w-5" />
        </div>
      </div>
      <div className={`absolute bottom-0 left-0 h-0.5 w-full ${accentClass.replace('/20', '')} opacity-60`} />
    </div>
  )
}
