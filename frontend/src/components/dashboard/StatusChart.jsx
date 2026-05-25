import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'

const COLORS = {
  PENDING: '#f59e0b',
  APPROVED: '#22c55e',
  REJECTED: '#ef4444',
}

export default function StatusChart({ byStatus = {} }) {
  const data = Object.entries(byStatus).map(([name, value]) => ({
    name: name.charAt(0) + name.slice(1).toLowerCase(),
    value,
    key: name,
  }))

  if (!data.length) {
    return <p className="py-12 text-center text-sm text-slate-500">No status data</p>
  }

  return (
    <ResponsiveContainer width="100%" height={220}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={52}
          outerRadius={78}
          paddingAngle={2}
          dataKey="value"
        >
          {data.map((entry) => (
            <Cell key={entry.key} fill={COLORS[entry.key] || '#64748b'} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{ background: '#1c2128', border: '1px solid #30363d', borderRadius: 8 }}
        />
        <Legend wrapperStyle={{ fontSize: 12, color: '#94a3b8' }} />
      </PieChart>
    </ResponsiveContainer>
  )
}
