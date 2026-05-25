import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts'
import { SOURCE_LABELS } from '../../utils/labels'

const COLORS = { SAP: '#8b5cf6', UTILITY: '#f59e0b', TRAVEL: '#22d3ee' }

export default function SourceChart({ bySource = {} }) {
  const data = Object.entries(bySource).map(([key, count]) => ({
    name: SOURCE_LABELS[key] || key,
    count,
    fill: COLORS[key] || '#3d9eff',
  }))

  if (!data.length) {
    return <p className="py-12 text-center text-sm text-slate-500">No source data</p>
  }

  return (
    <ResponsiveContainer width="100%" height={220}>
      <BarChart data={data} margin={{ top: 8, right: 8, left: -16, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#30363d" vertical={false} />
        <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
        <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
        <Tooltip
          contentStyle={{ background: '#1c2128', border: '1px solid #30363d', borderRadius: 8 }}
          labelStyle={{ color: '#e2e8f0' }}
        />
        <Bar dataKey="count" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  )
}
