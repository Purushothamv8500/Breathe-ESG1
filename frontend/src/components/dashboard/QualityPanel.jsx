import { AlertTriangle, Ruler, TrendingUp } from 'lucide-react'

const items = [
  { key: 'missing_fields', label: 'Missing fields', icon: AlertTriangle, color: 'border-amber-500/40 bg-amber-500/10 text-amber-300' },
  { key: 'invalid_units', label: 'Unit conversion issues', icon: Ruler, color: 'border-blue-500/40 bg-blue-500/10 text-blue-300' },
  { key: 'suspicious_values', label: 'Suspicious values (outliers)', icon: TrendingUp, color: 'border-red-500/40 bg-red-500/10 text-red-300' },
]

export default function QualityPanel({ quality = {} }) {
  return (
    <section>
      <h2 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-400">
        Data Quality Issues
      </h2>
      <div className="grid gap-4 sm:grid-cols-3">
        {items.map(({ key, label, icon: Icon, color }) => (
          <div
            key={key}
            className={`flex items-start gap-4 rounded-xl border p-4 ${color}`}
          >
            <Icon className="mt-0.5 h-5 w-5 shrink-0 opacity-80" />
            <div>
              <p className="text-2xl font-bold text-white">{quality[key] ?? 0}</p>
              <p className="mt-1 text-sm opacity-90">{label}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}
