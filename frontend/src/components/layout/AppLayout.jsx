import { useCallback, useEffect, useState } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import TopBar from './TopBar'
import { api, getClientId } from '../../api/client'

export default function AppLayout() {
  const [clientId, setClientIdState] = useState(getClientId())
  const [stats, setStats] = useState(null)
  const [apiError, setApiError] = useState(null)

  const refreshStats = useCallback(() => {
    api.dashboard()
      .then((data) => {
        setStats(data)
        setApiError(null)
      })
      .catch((err) => {
        console.error('API Error:', err)
        setStats(null)
        setApiError('Failed to connect to backend API')
      })
  }, [])

  useEffect(() => {
    refreshStats()
  }, [clientId, refreshStats])

  const handleClientChange = (id) => {
    setClientIdState(id)
    refreshStats()
  }

  return (
    <div className="min-h-screen bg-surface">
      <Sidebar />

      <div className="pl-56">
        <TopBar
          stats={stats}
          clientId={clientId}
          onClientChange={handleClientChange}
        />

        <main className="p-6">
          {apiError && (
            <div className="mb-4 rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-200">
              {apiError}
            </div>
          )}

          <Outlet context={{ refreshStats, stats }} />
        </main>
      </div>
    </div>
  )
}