import { Link, useNavigate, useLocation } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()
  const location = useLocation()

  function logout() {
    localStorage.removeItem('token')
    navigate('/login')
  }

  function isActive(path) {
    return location.pathname === path
  }

  return (
    <nav style={{
      background: 'var(--surface)',
      borderBottom: '1px solid var(--border)',
      padding: '0 2rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      height: '52px',
      position: 'sticky',
      top: 0,
      zIndex: 100
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
        <Link to="/" style={{
          color: 'var(--text)',
          fontWeight: 600,
          fontSize: '15px',
          textDecoration: 'none',
          fontFamily: 'var(--mono)',
          letterSpacing: '-0.02em'
        }}>
          ⬡ SentinelPy
        </Link>

        <div style={{ display: 'flex', gap: '4px' }}>
          {[
            { label: 'Dashboard', path: '/' },
            { label: 'New Scan', path: '/scan/new' },
            { label: 'History', path: '/scan/history' },
          ].map(({ label, path }) => (
            <Link key={path} to={path} style={{
              padding: '4px 12px',
              borderRadius: '6px',
              fontSize: '13px',
              textDecoration: 'none',
              color: isActive(path) ? 'var(--text)' : 'var(--muted)',
              background: isActive(path) ? 'var(--surface2)' : 'transparent',
              transition: 'all 0.15s'
            }}>
              {label}
            </Link>
          ))}
        </div>
      </div>

      <button onClick={logout} className="btn-ghost" style={{ padding: '4px 12px', fontSize: '13px' }}>
        Sign out
      </button>
    </nav>
  )
}
