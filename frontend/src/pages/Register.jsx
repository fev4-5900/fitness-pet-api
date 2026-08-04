import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api, setToken } from '../api'
import Chinchilla from '../components/Chinchilla'
import Scene from '../components/Scene'

export default function Register() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    phone_number: '',
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  function set(name) {
    return (e) => setForm((f) => ({ ...f, [name]: e.target.value }))
  }

  async function submit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await api.register({ ...form, role: 'user' })
      const res = await api.login(form.username, form.password)
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
          <Chinchilla mood="happy" size={150} />
        </Scene>
      </div>
      <div className="auth-panel panel">
        <h1 className="pixel-title">NEW<br />TRAINER</h1>
        <p className="sub">create an account to meet your chinchilla buddy</p>
        <form onSubmit={submit} className="stack">
          <div className="row2">
            <label className="field">
              <span>FIRST NAME</span>
              <input className="pinput" value={form.first_name} onChange={set('first_name')} required />
            </label>
            <label className="field">
              <span>LAST NAME</span>
              <input className="pinput" value={form.last_name} onChange={set('last_name')} required />
            </label>
          </div>
          <label className="field">
            <span>USERNAME</span>
            <input className="pinput" value={form.username} onChange={set('username')} required />
          </label>
          <label className="field">
            <span>EMAIL</span>
            <input className="pinput" type="email" value={form.email} onChange={set('email')} required />
          </label>
          <label className="field">
            <span>PHONE</span>
            <input className="pinput" value={form.phone_number} onChange={set('phone_number')} required />
          </label>
          <label className="field">
            <span>PASSWORD</span>
            <input className="pinput" type="password" value={form.password} onChange={set('password')} minLength={6} required />
          </label>
          {error && <p className="error-text">{error}</p>}
          <button type="submit" className="pbtn" disabled={loading}>
            {loading ? '...' : 'CREATE ACCOUNT'}
          </button>
        </form>
        <p className="switch-text">
          GOT AN ACCOUNT? <Link to="/login">LOG IN</Link>
        </p>
      </div>
    </div>
  )
}
