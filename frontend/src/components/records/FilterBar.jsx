import { Search } from 'lucide-react'

export default function FilterBar({ filters, onChange, search, onSearchChange }) {
  return (
    <div className="flex flex-wrap items-center gap-3 rounded-xl border border-surface-border bg-surface-raised p-4">
      <div className="relative min-w-[200px] flex-1">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
        <input
          type="search"
          placeholder="Search description, category, location…"
          value={search}
          onChange={(e) => onSearchChange(e.target.value)}
          className="w-full rounded-lg border border-surface-border bg-surface py-2 pl-9 pr-3 text-sm text-slate-200 placeholder:text-slate-600 focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent"
        />
      </div>
      <select
        value={filters.source}
        onChange={(e) => onChange({ ...filters, source: e.target.value })}
        className="rounded-lg border border-surface-border bg-surface px-3 py-2 text-sm text-slate-200"
      >
        <option value="">All sources</option>
        <option value="SAP">SAP</option>
        <option value="UTILITY">Utility</option>
        <option value="TRAVEL">Travel</option>
      </select>
      <select
        value={filters.status}
        onChange={(e) => onChange({ ...filters, status: e.target.value })}
        className="rounded-lg border border-surface-border bg-surface px-3 py-2 text-sm text-slate-200"
      >
        <option value="">All statuses</option>
        <option value="PENDING">Pending</option>
        <option value="APPROVED">Approved</option>
        <option value="REJECTED">Rejected</option>
      </select>
      <select
        value={filters.scope}
        onChange={(e) => onChange({ ...filters, scope: e.target.value })}
        className="rounded-lg border border-surface-border bg-surface px-3 py-2 text-sm text-slate-200"
      >
        <option value="">All scopes</option>
        <option value="SCOPE_1">Scope 1</option>
        <option value="SCOPE_2">Scope 2</option>
        <option value="SCOPE_3">Scope 3</option>
      </select>
    </div>
  )
}
