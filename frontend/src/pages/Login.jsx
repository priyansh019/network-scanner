import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { auth } from '../api'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  async function handleLogin(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await auth.login(email, password)
      localStorage.setItem('token', res.data.access_token)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Check your credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'var(--bg)'
    }}>
      <div style={{ width: '100%', maxWidth: '380px', padding: '0 1rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{
            fontFamily: 'var(--mono)',
            fontSize: '22px',
            fontWeight: 600,
            marginBottom: '8px'
          }}>
            ⬡ SentinelPy
          </div>
          <p style={{ color: 'var(--muted)', fontSize: '13px' }}>
            Network Security Scanning Platform
          </p>
        </div>

        <div className="card">
          <h2 style={{ fontSize: '16px', fontWeight: 500, marginBottom: '1.25rem' }}>
            Sign in
          </h2>

          <form onSubmit={handleLogin}>
            <div style={{ marginBottom: '12px' }}>
              <label className="label">Email</label>
              <input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
              />
            </div>

            <div style={{ marginBottom: '16px' }}>
              <label className="label">Password</label>
              <input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={e => setPassword(e.target.value)}
                required
              />
            </div>

            <button
              type="submit"
              className="btn-primary w-full"
              disabled={loading}
              style={{ padding: '10px' }}
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>

            {error && <div className="error-msg">{error}</div>}
          </form>

          <p style={{ textAlign: 'center', marginTop: '16px', fontSize: '13px', color: 'var(--muted)' }}>
            No account? <Link to="/register">Create one</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
