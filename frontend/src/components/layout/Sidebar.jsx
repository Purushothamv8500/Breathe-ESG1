import { NavLink } from 'react-router-dom'
import { LayoutDashboard, Table2, ClipboardList, Leaf } from 'lucide-react'

const nav = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/records', icon: Table2, label: 'Records' },
  { to: '/pending', icon: ClipboardList, label: 'Pending Reviews' },
]

export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 z-30 flex h-screen w-56 flex-col border-r border-surface-border bg-surface-raised">
      <div className="flex items-center gap-2 border-b border-surface-border px-5 py-5">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-accent/20 text-accent">
          <Leaf className="h-5 w-5" />
        </div>
        <div>
          <p className="text-sm font-semibold text-white">Breathe ESG</p>
          <p className="text-xs text-slate-500">Analyst Console</p>
        </div>
      </div>
      <nav className="flex-1 space-y-1 px-3 py-4">
        {nav.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-accent/15 text-accent'
                  : 'text-slate-400 hover:bg-surface-overlay hover:text-slate-200'
              }`
            }
          >
            <Icon className="h-4 w-4 shrink-0" />
            {label}
          </NavLink>
        ))}
      </nav>
      <div className="border-t border-surface-border px-4 py-4 text-xs text-slate-500">
        Internal review tool
      </div>
    </aside>
  )
}
