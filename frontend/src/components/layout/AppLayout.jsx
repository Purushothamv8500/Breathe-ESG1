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
        setStats(null)
        setApiError(err.message || 'Cannot reach API')
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
        <TopBar stats={stats} clientId={clientId} onClientChange={handleClientChange} />
        <main className="p-6">
          {apiError && (
            <div className="mb-4 rounded-lg border border-amber-500/40 bg-amber-500/10 px-4 py-3 text-sm text-amber-200">
              <strong>Backend not connected.</strong> The Django API must be running on port{' '}
              <strong>8001</strong>. In a new terminal run:{' '}
              <code className="rounded bg-black/30 px-1.5 py-0.5 text-xs">
                .\start-backend.ps1
              </code>
              {' '}from the project root, then hard-refresh this page (Ctrl+Shift+R).
            </div>
          )}
          <Outlet context={{ refreshStats, stats }} />
        </main>
      </div>
    </div>
  )
}
