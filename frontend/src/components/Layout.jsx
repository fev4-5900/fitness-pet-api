import { NavLink, useNavigate } from 'react-router-dom'
import PixelIcon from './PixelIcon'
import { setToken } from '../api'

const LINKS = [
  { to: '/dashboard', icon: 'home', label: 'HOME' },
  { to: '/log', icon: 'plus', label: 'LOG' },
  { to: '/targets', icon: 'target', label: 'GOALS' },
  { to: '/profile', icon: 'profile', label: 'ME' },
]

export default function Layout({ children }) {
  const navigate = useNavigate()

  function logout() {
    setToken(null)
    navigate('/login')
  }

  return (
    <div className="layout">
      <header className="navbar">
        <NavLink to="/dashboard" className="brand">
          <PixelIcon name="paw" size={26} />
          <span>FIT PET</span>
        </NavLink>
        <nav className="navlinks">
          {LINKS.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              className={({ isActive }) => `navlink ${isActive ? 'active' : ''}`}
            >
              <PixelIcon name={l.icon} size={20} />
              <span>{l.label}</span>
            </NavLink>
          ))}
          <button type="button" className="navlink navbtn" onClick={logout}>
            <PixelIcon name="logout" size={20} />
            <span>OUT</span>
          </button>
        </nav>
      </header>
      <main className="content">{children}</main>
    </div>
  )
}
