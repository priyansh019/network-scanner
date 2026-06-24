import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { scans } from '../api'
import RiskBadge, { StatusBadge } from '../components/RiskBadge'

export default function ScanHistory() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [skip, setSkip] = useState(0)
  const [status, setStatus] = useState('')
  const [target, setTarget] = useState('')
  const limit = 10

  async function load(newSkip = 0, newStatus = status, newTarget = target) {
    setLoading(true)
    try {
      const params = { skip: newSkip, limit }
      if (newStatus) params.status = newStatus
      if (newTarget) params.target = newTarget
      const res = await scans.history(params)
      setData(res.data)
      setSkip(newSkip)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  function handleFilter(e) {
    e.preventDefault()
    load(0, status, target)
  }

  function handleClear() {
    setStatus('')
    setTarget('')
    load(0, '', '')
  }

  return (
    <div className="page">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 style={{ fontSize: '20px', fontWeight: 600 }}>Scan history</h1>
          <p style={{ color: 'var(--muted)', fontSize: '13px', marginTop: '2px' }}>
            All network scans
          </p>
        </div>
        <Link to="/scan/new">
          <button className="btn-primary">+ New Scan</button>
        </Link>
      </div>

      <div className="card" style={{ marginBottom: '16px' }}>
        <form onSubmit={handleFilter} style={{ display: 'flex', gap: '12px', alignItems: 'flex-end' }}>
          <div style={{ flex: 1 }}>
            <label className="label">Filter by target</label>
            <input
              type="text"
              placeholder="192.168..."
              value={target}
              onChange={e => setTarget(e.target.value)}
              style={{ fontFamily: 'var(--mono)' }}
            />
          </div>
          <div style={{ width: '160px' }}>
            <label className="label">Status</label>
            <select value={status} onChange={e => setStatus(e.target.value)}>
              <option value="">All statuses</option>
              <option value="initiated">Initiated</option>
              <option value="processing">Processing</option>
              <option value="completed">Completed</option>
              <option value="failed">Failed</option>
            </select>
          </div>
          <button type="submit" className="btn-primary" style={{ whiteSpace: 'nowrap' }}>
            Filter
          </button>
          <button type="button" className="btn-ghost" onClick={handleClear}>
            Clear
          </button>
        </form>
      </div>

      <div className="card">
        {loading ? (
          <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--muted)' }}>
            <div className="spinner" style={{ margin: '0 auto 8px' }}></div>
            <div style={{ fontSize: '13px' }}>Loading...</div>
          </div>
        ) : data.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--muted)' }}>
            <div style={{ fontSize: '14px' }}>No scans found</div>
          </div>
        ) : (
          <>
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Target</th>
                  <th>Ports requested</th>
                  <th>Open</th>
                  <th>Risk</th>
                  <th>Status</th>
                  <th>Date</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {data.map(scan => (
                  <tr key={scan.id}>
                    <td className="mono" style={{ color: 'var(--muted)' }}>#{scan.id}</td>
                    <td className="mono">{scan.target}</td>
                    <td className="mono" style={{ color: 'var(--muted)', fontSize: '12px' }}>
                      {scan.ports}
                    </td>
                    <td className="mono">
                      {scan.open_ports ? scan.open_ports.length : '—'}
                    </td>
                    <td>
                      {scan.risk_level ? <RiskBadge level={scan.risk_level} /> : '—'}
                    </td>
                    <td><StatusBadge status={scan.status} /></td>
                    <td style={{ color: 'var(--muted)', fontSize: '12px' }}>
                      {new Date(scan.created_at).toLocaleString()}
                    </td>
                    <td>
                      <Link to={`/scan/${scan.id}`} style={{ fontSize: '12px' }}>View →</Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginTop: '16px',
              paddingTop: '16px',
              borderTop: '1px solid var(--border)'
            }}>
              <div style={{ fontSize: '12px', color: 'var(--muted)' }}>
                Showing {skip + 1}–{skip + data.length}
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button
                  className="btn-ghost"
                  style={{ padding: '4px 12px', fontSize: '13px' }}
                  disabled={skip === 0}
                  onClick={() => load(skip - limit)}
                >
                  ← Prev
                </button>
                <button
                  className="btn-ghost"
                  style={{ padding: '4px 12px', fontSize: '13px' }}
                  disabled={data.length < limit}
                  onClick={() => load(skip + limit)}
                >
                  Next →
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
