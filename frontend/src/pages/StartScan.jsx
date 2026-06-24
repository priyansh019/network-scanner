import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { scans } from '../api'

const PRESET_PORTS = {
  'Common (Top 11)': [21, 22, 23, 25, 53, 80, 443, 3306, 5432, 8080, 8443],
  'Web only': [80, 443, 8080, 8443],
  'Database': [3306, 5432, 1433, 27017, 6379],
  'Remote access': [22, 23, 3389, 5900],
}

export default function StartScan() {
  const [target, setTarget] = useState('')
  const [portsInput, setPortsInput] = useState('21, 22, 23, 25, 53, 80, 443, 3306, 5432, 8080, 8443')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(null)
  const navigate = useNavigate()

  function applyPreset(preset) {
    setPortsInput(PRESET_PORTS[preset].join(', '))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const ports = portsInput.split(',').map(p => parseInt(p.trim())).filter(p => !isNaN(p))

      if (ports.length === 0) {
        setError('Enter at least one valid port number.')
        setLoading(false)
        return
      }

      const res = await scans.start(target, ports)
      setSuccess(res.data)

      setTimeout(() => {
        navigate(`/scan/${res.data.scan_id}`)
      }, 1500)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start scan.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page" style={{ maxWidth: '600px' }}>
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '20px', fontWeight: 600 }}>New scan</h1>
        <p style={{ color: 'var(--muted)', fontSize: '13px', marginTop: '2px' }}>
          Enter a target IP or hostname to scan
        </p>
      </div>

      <div className="card">
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '20px' }}>
            <label className="label">Target IP or hostname</label>
            <input
              type="text"
              placeholder="192.168.1.1 or scanme.nmap.org"
              value={target}
              onChange={e => setTarget(e.target.value)}
              required
              style={{ fontFamily: 'var(--mono)' }}
            />
            <div style={{ fontSize: '12px', color: 'var(--muted)', marginTop: '4px' }}>
              Only scan targets you have permission to scan.
            </div>
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label className="label">Ports</label>
            <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginBottom: '8px' }}>
              {Object.keys(PRESET_PORTS).map(preset => (
                <button
                  key={preset}
                  type="button"
                  className="btn-ghost"
                  style={{ padding: '3px 10px', fontSize: '12px' }}
                  onClick={() => applyPreset(preset)}
                >
                  {preset}
                </button>
              ))}
            </div>
            <input
              type="text"
              placeholder="22, 80, 443, 8080"
              value={portsInput}
              onChange={e => setPortsInput(e.target.value)}
              style={{ fontFamily: 'var(--mono)' }}
            />
            <div style={{ fontSize: '12px', color: 'var(--muted)', marginTop: '4px' }}>
              Comma-separated port numbers
            </div>
          </div>

          <div style={{
            background: 'var(--surface2)',
            border: '1px solid var(--border)',
            borderRadius: '6px',
            padding: '12px',
            marginBottom: '20px',
            fontSize: '12px',
            color: 'var(--muted)'
          }}>
            <strong style={{ color: 'var(--warning)' }}>⚠ Notice:</strong> After starting a scan here,
            run the scanner engine manually with the returned scan ID to execute the real scan.
            The backend will save results automatically when the scanner finishes.
          </div>

          <button
            type="submit"
            className="btn-primary w-full"
            disabled={loading}
            style={{ padding: '10px' }}
          >
            {loading ? 'Starting scan...' : 'Start scan →'}
          </button>

          {error && <div className="error-msg">{error}</div>}

          {success && (
            <div className="success-msg">
              Scan #{success.scan_id} created for <span className="mono">{success.target}</span>.
              Redirecting to results...
            </div>
          )}
        </form>
      </div>
    </div>
  )
}
