import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api, setToken } from '../api'
import Chinchilla from '../components/Chinchilla'
import Scene from '../components/Scene'

export default function Login() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function submit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await api.login(username.trim(), password)
      setToken(res.access_token)
      navigate('/dashboard')
    } catch (err) {
      setError(err.message)
      setLoading(false)
    }
  }

  return (
    <div className="auth-wrap">
      <div className="auth-scene">
        <Scene>
          <Chinchilla mood="ok" size={170} />
        </Scene>
      </div>
      <div className="auth-panel panel">
        <h1 className="pixel-title">FIT PET</h1>
        <p className="sub">your cozy pixel workout buddy</p>
        <form onSubmit={submit} className="stack">
          <label className="field">
            <span>USERNAME</span>
            <input
              className="pinput"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
              required
            />
          </label>
          <label className="field">
            <span>PASSWORD</span>
            <input
              className="pinput"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              required
            />
          </label>
          {error && <p className="error-text">{error}</p>}
          <button type="submit" className="pbtn" disabled={loading}>
            {loading ? '...' : 'ENTER'}
          </button>
        </form>
        <p className="switch-text">
          NEW HERE? <Link to="/register">MAKE AN ACCOUNT</Link>
        </p>
      </div>
    </div>
  )
}
