import { useEffect, useState } from 'react'
import { useOutletContext } from 'react-router-dom'
import { Database, Clock, CheckCircle2, XCircle } from 'lucide-react'
import { api } from '../api/client'
import KpiCard from '../components/dashboard/KpiCard'
import SourceChart from '../components/dashboard/SourceChart'
import StatusChart from '../components/dashboard/StatusChart'
import QualityPanel from '../components/dashboard/QualityPanel'

export default function Dashboard() {
  const { stats: layoutStats } = useOutletContext() || {}
  const [data, setData] = useState(layoutStats)
  const [error, setError] = useState(null)

  useEffect(() => {
    api.dashboard().then(setData).catch((e) => setError(e.message))
  }, [])

  useEffect(() => {
    if (layoutStats) setData(layoutStats)
  }, [layoutStats])

  if (error) {
    return (
      <div className="rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-red-300">
        {error}
      </div>
    )
  }

  if (!data) {
    return <p className="text-slate-500">Loading dashboard…</p>
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Dashboard</h1>
        <p className="mt-1 text-sm text-slate-500">
          Emissions data ingestion overview and quality insights
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <KpiCard
          title="Total Records"
          value={data.total}
          icon={Database}
          gradientClass="gradient-kpi-total"
          accentClass="bg-accent/20 text-accent"
        />
        <KpiCard
          title="Pending Review"
          value={data.pending}
          icon={Clock}
          gradientClass="gradient-kpi-pending"
          accentClass="bg-amber-500/20 text-amber-400"
        />
        <KpiCard
          title="Approved"
          value={data.approved}
          icon={CheckCircle2}
          gradientClass="gradient-kpi-approved"
          accentClass="bg-emerald-500/20 text-emerald-400"
        />
        <KpiCard
          title="Rejected"
          value={data.rejected}
          icon={XCircle}
          gradientClass="gradient-kpi-rejected"
          accentClass="bg-red-500/20 text-red-400"
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-surface-border bg-surface-raised p-5 shadow-card">
          <h2 className="mb-4 text-sm font-semibold text-slate-300">Records by Source</h2>
          <SourceChart bySource={data.by_source} />
        </div>
        <div className="rounded-xl border border-surface-border bg-surface-raised p-5 shadow-card">
          <h2 className="mb-4 text-sm font-semibold text-slate-300">Status Distribution</h2>
          <StatusChart byStatus={data.by_status} />
        </div>
      </div>

      <QualityPanel quality={data.quality} />
    </div>
  )
}
