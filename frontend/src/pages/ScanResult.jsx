import { useState, useEffect, useRef } from 'react'
import { useParams, Link } from 'react-router-dom'
import { scans } from '../api'
import RiskBadge, { StatusBadge } from '../components/RiskBadge'

const RISK_COLORS = {
  low: 'var(--success)',
  medium: 'var(--warning)',
  high: 'var(--danger)',
  critical: 'var(--critical)',
}

const DANGEROUS_PORTS = [21, 23, 3306, 5432, 1433, 27017]

export default function ScanResult() {
  const { id } = useParams()
  const [scan, setScan] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const pollingRef = useRef(null)

  async function fetchScan() {
    try {
      const res = await scans.getById(id)
      setScan(res.data)

      if (res.data.status === 'initiated' || res.data.status === 'processing') {
        pollingRef.current = setTimeout(fetchScan, 3000)
      }
    } catch (err) {
      setError('Scan not found.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchScan()
    return () => { if (pollingRef.current) clearTimeout(pollingRef.current) }
  }, [id])

  if (loading) return (
    <div className="page" style={{ textAlign: 'center', paddingTop: '4rem' }}>
      <div className="spinner" style={{ margin: '0 auto 12px' }}></div>
      <div style={{ color: 'var(--muted)' }}>Loading scan...</div>
    </div>
  )

  if (error) return (
    <div className="page" style={{ textAlign: 'center', paddingTop: '4rem' }}>
      <div style={{ color: 'var(--danger)', marginBottom: '16px' }}>{error}</div>
      <Link to="/scan/history"><button className="btn-ghost">← Back to history</button></Link>
    </div>
  )

  const isProcessing = scan.status === 'initiated' || scan.status === 'processing'

  return (
    <div className="page">
      <div style={{ marginBottom: '1.5rem' }}>
        <Link to="/scan/history" style={{ fontSize: '13px', color: 'var(--muted)' }}>
          ← Scan history
        </Link>
      </div>

      <div className="flex items-center justify-between mb-6">
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <h1 style={{ fontFamily: 'var(--mono)', fontSize: '20px', fontWeight: 600 }}>
              {scan.target}
            </h1>
            <StatusBadge status={scan.status} />
            {scan.risk_level && <RiskBadge level={scan.risk_level} />}
          </div>
          <p style={{ color: 'var(--muted)', fontSize: '12px', marginTop: '4px', fontFamily: 'var(--mono)' }}>
            Scan #{scan.id} · {new Date(scan.created_at).toLocaleString()}
          </p>
        </div>
        <Link to="/scan/new">
          <button className="btn-ghost" style={{ fontSize: '13px' }}>+ New scan</button>
        </Link>
      </div>

      {isProcessing && (
        <div style={{
          background: 'rgba(47, 129, 247, 0.08)',
          border: '1px solid rgba(47, 129, 247, 0.25)',
          borderRadius: '8px',
          padding: '14px 16px',
          marginBottom: '20px',
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <div className="spinner" style={{ flexShrink: 0 }}></div>
          <div>
            <div style={{ fontSize: '14px', fontWeight: 500 }}>Scan in progress</div>
            <div style={{ fontSize: '12px', color: 'var(--muted)', marginTop: '2px' }}>
              Auto-refreshing every 3 seconds. Run the scanner engine with scan ID <span className="mono">#{scan.id}</span>.
            </div>
          </div>
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px', marginBottom: '20px' }}>
        <div className="card">
          <div style={{ fontSize: '12px', color: 'var(--muted)', marginBottom: '6px' }}>Open ports</div>
          <div style={{ fontSize: '28px', fontWeight: 600, fontFamily: 'var(--mono)', color: 'var(--accent)' }}>
            {scan.open_ports ? scan.open_ports.length : '—'}
          </div>
        </div>
        <div className="card">
          <div style={{ fontSize: '12px', color: 'var(--muted)', marginBottom: '6px' }}>Risk level</div>
          <div style={{ fontSize: '28px', fontWeight: 600, fontFamily: 'var(--mono)', color: RISK_COLORS[scan.risk_level] || 'var(--muted)' }}>
            {scan.risk_level || '—'}
          </div>
        </div>
        <div className="card">
          <div style={{ fontSize: '12px', color: 'var(--muted)', marginBottom: '6px' }}>Status</div>
          <div style={{ fontSize: '18px', fontWeight: 600, fontFamily: 'var(--mono)', marginTop: '4px' }}>
            <StatusBadge status={scan.status} />
          </div>
        </div>
      </div>

      {scan.open_ports && scan.open_ports.length > 0 && (
        <div className="card" style={{ marginBottom: '16px' }}>
          <h2 style={{ fontSize: '15px', fontWeight: 500, marginBottom: '16px' }}>
            Open ports
          </h2>
          <table>
            <thead>
              <tr>
                <th>Port</th>
                <th>Service</th>
                <th>Risk indicator</th>
              </tr>
            </thead>
            <tbody>
              {scan.open_ports.map(port => {
                const service = scan.services?.[String(port)] || 'Unknown'
                const isDangerous = DANGEROUS_PORTS.includes(port)
                return (
                  <tr key={port}>
                    <td>
                      <span className="mono" style={{ fontWeight: 500 }}>{port}</span>
                    </td>
                    <td className="mono">{service}</td>
                    <td>
                      {isDangerous ? (
                        <span className="badge badge-high">dangerous</span>
                      ) : (
                        <span className="badge badge-low">ok</span>
                      )}
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}

      {scan.status === 'completed' && (!scan.open_ports || scan.open_ports.length === 0) && (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <div style={{ fontSize: '32px', marginBottom: '8px' }}>✓</div>
          <div style={{ fontWeight: 500, marginBottom: '4px' }}>No open ports found</div>
          <div style={{ color: 'var(--muted)', fontSize: '13px' }}>
            All scanned ports are closed or filtered.
          </div>
        </div>
      )}

      <div className="card">
        <h2 style={{ fontSize: '15px', fontWeight: 500, marginBottom: '12px' }}>Scan details</h2>
        <table>
          <tbody>
            <tr>
              <td style={{ color: 'var(--muted)', width: '140px' }}>Target</td>
              <td className="mono">{scan.target}</td>
            </tr>
            <tr>
              <td style={{ color: 'var(--muted)' }}>Ports requested</td>
              <td className="mono" style={{ fontSize: '12px' }}>{scan.ports}</td>
            </tr>
            <tr>
              <td style={{ color: 'var(--muted)' }}>Status</td>
              <td><StatusBadge status={scan.status} /></td>
            </tr>
            <tr>
              <td style={{ color: 'var(--muted)' }}>Risk level</td>
              <td>{scan.risk_level ? <RiskBadge level={scan.risk_level} /> : '—'}</td>
            </tr>
            <tr>
              <td style={{ color: 'var(--muted)' }}>Created</td>
              <td style={{ color: 'var(--muted)', fontFamily: 'var(--mono)', fontSize: '12px' }}>
                {new Date(scan.created_at).toLocaleString()}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}
