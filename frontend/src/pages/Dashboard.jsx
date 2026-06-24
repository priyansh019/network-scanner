import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { scans } from '../api'
import RiskBadge, { StatusBadge } from '../components/RiskBadge'

function StatCard({ label, value, color }) {
  return (
    <div style={{
      background: 'var(--surface)',
      border: '1px solid var(--border)',
      borderRadius: '8px',
      padding: '1rem 1.25rem'
    }}>
      <div style={{ fontSize: '12px', color: 'var(--muted)', marginBottom: '6px' }}>{label}</div>
      <div style={{ fontSize: '28px', fontWeight: 600, fontFamily: 'var(--mono)', color: color || 'var(--text)' }}>
        {value}
      </div>
    </div>
  )
}

export default function Dashboard() {
  const [recentScans, setRecentScans] = useState([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({ total: 0, completed: 0, critical: 0, processing: 0 })

  useEffect(() => {
    async function load() {
      try {
        const res = await scans.history({ limit: 10, skip: 0 })
        const data = res.data
        setRecentScans(data)
        setStats({
          total: data.length,
          completed: data.filter(s => s.status === 'completed').length,
          critical: data.filter(s => s.risk_level === 'critical' || s.risk_level === 'high').length,
          processing: data.filter(s => s.status === 'processing' || s.status === 'initiated').length,
        })
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return (
    <div className="page">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 style={{ fontSize: '20px', fontWeight: 600 }}>Dashboard</h1>
          <p style={{ color: 'var(--muted)', fontSize: '13px', marginTop: '2px' }}>
            Network security scan overview
          </p>
        </div>
        <Link to="/scan/new">
          <button className="btn-primary">+ New Scan</button>
        </Link>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px', marginBottom: '2rem' }}>
        <StatCard label="Total scans" value={stats.total} />
        <StatCard label="Completed" value={stats.completed} color="var(--success)" />
        <StatCard label="High / Critical" value={stats.critical} color="var(--danger)" />
        <StatCard label="In progress" value={stats.processing} color="var(--warning)" />
      </div>

      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 style={{ fontSize: '15px', fontWeight: 500 }}>Recent scans</h2>
          <Link to="/scan/history" style={{ fontSize: '13px' }}>View all →</Link>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--muted)' }}>
            <div className="spinner" style={{ margin: '0 auto 8px' }}></div>
            <div style={{ fontSize: '13px' }}>Loading scans...</div>
          </div>
        ) : recentScans.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--muted)' }}>
            <div style={{ fontSize: '32px', marginBottom: '8px' }}>⬡</div>
            <div style={{ fontSize: '14px', marginBottom: '16px' }}>No scans yet</div>
            <Link to="/scan/new">
              <button className="btn-primary">Start your first scan</button>
            </Link>
          </div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Target</th>
                <th>Open ports</th>
                <th>Risk</th>
                <th>Status</th>
                <th>Date</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {recentScans.map(scan => (
                <tr key={scan.id}>
                  <td className="mono" style={{ color: 'var(--muted)' }}>#{scan.id}</td>
                  <td className="mono">{scan.target}</td>
                  <td className="mono">
                    {scan.open_ports ? scan.open_ports.length : '—'}
                  </td>
                  <td>
                    {scan.risk_level ? <RiskBadge level={scan.risk_level} /> : '—'}
                  </td>
                  <td><StatusBadge status={scan.status} /></td>
                  <td style={{ color: 'var(--muted)', fontSize: '12px' }}>
                    {new Date(scan.created_at).toLocaleDateString()}
                  </td>
                  <td>
                    <Link to={`/scan/${scan.id}`} style={{ fontSize: '12px' }}>
                      View →
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

