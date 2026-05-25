import { useCallback, useEffect, useMemo, useState } from 'react'
import { useOutletContext, useSearchParams } from 'react-router-dom'
import { api, unwrapRecords } from '../api/client'
import FilterBar from '../components/records/FilterBar'
import RecordsGrid from '../components/records/RecordsGrid'
import RecordDrawer from '../components/records/RecordDrawer'

export default function Records() {
  const { refreshStats } = useOutletContext() || {}
  const [searchParams] = useSearchParams()
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [search, setSearch] = useState('')
  const [selectedId, setSelectedId] = useState(null)
  const [filters, setFilters] = useState({
    source: searchParams.get('source') || '',
    status: searchParams.get('status') || '',
    scope: searchParams.get('scope') || '',
  })

  const load = useCallback(() => {
    setLoading(true)
    const params = {}
    if (filters.source) params.source = filters.source
    if (filters.status) params.status = filters.status
    if (filters.scope) params.scope = filters.scope
    api
      .records(params)
      .then((data) => setRecords(unwrapRecords(data)))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [filters])

  useEffect(() => {
    load()
  }, [load])

  const filtered = useMemo(() => {
    if (!search.trim()) return records
    const q = search.toLowerCase()
    return records.filter(
      (r) =>
        (r.description || '').toLowerCase().includes(q) ||
        (r.category || '').toLowerCase().includes(q) ||
        (r.location || '').toLowerCase().includes(q) ||
        String(r.id).includes(q),
    )
  }, [records, search])

  const handleUpdated = () => {
    load()
    refreshStats?.()
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Records</h1>
        <p className="mt-1 text-sm text-slate-500">
          Review normalized emissions — click a row to inspect raw vs processed data
        </p>
      </div>

      <FilterBar
        filters={filters}
        onChange={setFilters}
        search={search}
        onSearchChange={setSearch}
      />

      {error && (
        <div className="rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-300">
          {error}
        </div>
      )}

      {loading ? (
        <p className="text-slate-500">Loading records…</p>
      ) : (
        <RecordsGrid
          records={filtered}
          onRowClick={setSelectedId}
          selectedId={selectedId}
        />
      )}

      <RecordDrawer
        recordId={selectedId}
        onClose={() => setSelectedId(null)}
        onUpdated={handleUpdated}
      />
    </div>
  )
}
