import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api } from '../api'
import Chinchilla from '../components/Chinchilla'

const COLORS = [
  { name: 'CARAMEL', value: '#A8763E' },
  { name: 'MOCHA', value: '#6E4523' },
  { name: 'CREAM', value: '#C89A63' },
  { name: 'TOFFEE', value: '#8A5A2E' },
]

export default function CreatePet() {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [color, setColor] = useState(COLORS[0].value)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function submit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await api.createPet({ name: name.trim(), description: description.trim(), color })
      navigate('/dashboard')
    } catch (err) {
      setError(err.message)
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <h1 className="pixel-title">ADOPT A<br />CHINCHILLA</h1>
      <p className="sub">name your new workout buddy</p>
      <div className="pet-preview">
        <Chinchilla mood="happy" size={170} />
      </div>
      <form onSubmit={submit} className="panel stack maxw">
        <label className="field">
          <span>NAME</span>
          <input className="pinput" value={name} onChange={(e) => setName(e.target.value)} minLength={3} required />
        </label>
        <label className="field">
          <span>DESCRIPTION (OPTIONAL)</span>
          <input className="pinput" value={description} onChange={(e) => setDescription(e.target.value)} />
        </label>
        <div className="field">
          <span>FUR COLOR</span>
          <div className="swatches">
            {COLORS.map((c) => (
              <button
                key={c.value}
                type="button"
                className={`swatch ${color === c.value ? 'active' : ''}`}
                style={{ background: c.value }}
                onClick={() => setColor(c.value)}
                title={c.name}
              />
            ))}
          </div>
        </div>
        {error && <p className="error-text">{error}</p>}
        <div className="row2">
          <button type="submit" className="pbtn" disabled={loading}>
            {loading ? '...' : 'ADOPT'}
          </button>
          <Link to="/dashboard" className="pbtn pbtn-ghost">
            LATER
          </Link>
        </div>
      </form>
    </div>
  )
}
