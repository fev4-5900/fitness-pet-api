import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'

const EMPTY = { gender: '', height: '', weight: '', age: '', activity: '', goal: 'maintain' }

export default function Profile() {
  const [form, setForm] = useState(EMPTY)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    api
      .getProfile()
      .then((p) =>
        setForm({
          gender: p.gender || '',
          height: p.height ?? '',
          weight: p.weight ?? '',
          age: p.age ?? '',
          activity: p.activity ?? '',
          goal: p.goal || 'maintain',
        }),
      )
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  function set(name) {
    return (e) => setForm((f) => ({ ...f, [name]: e.target.value }))
  }

  async function submit(e) {
    e.preventDefault()
    setError('')
    setSaved(false)
    try {
      await api.saveProfile({
        gender: form.gender,
        height: parseFloat(form.height),
        weight: parseFloat(form.weight),
        age: parseFloat(form.age),
        activity: parseInt(form.activity, 10) || 0,
        goal: form.goal,
      })
      setSaved(true)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="page">
      <h1 className="pixel-title">MY PROFILE</h1>
      <p className="sub">this feeds the goal calculator</p>
      <form onSubmit={submit} className="panel stack maxw">
        <div className="row2">
          <label className="field">
            <span>GENDER</span>
            <select className="pinput" value={form.gender} onChange={set('gender')} required>
              <option value="">--</option>
              <option value="male">MALE</option>
              <option value="female">FEMALE</option>
            </select>
          </label>
          <label className="field">
            <span>GOAL</span>
            <select className="pinput" value={form.goal} onChange={set('goal')}>
              <option value="maintain">MAINTAIN</option>
              <option value="lose">LOSE</option>
              <option value="gain">GAIN</option>
            </select>
          </label>
        </div>
        <div className="row3">
          <label className="field">
            <span>HEIGHT (CM)</span>
            <input className="pinput" type="number" value={form.height} onChange={set('height')} required />
          </label>
          <label className="field">
            <span>WEIGHT (KG)</span>
            <input className="pinput" type="number" value={form.weight} onChange={set('weight')} required />
          </label>
          <label className="field">
            <span>AGE</span>
            <input className="pinput" type="number" value={form.age} onChange={set('age')} required />
          </label>
        </div>
        <label className="field">
          <span>TRAINING DAYS / WEEK (0-7)</span>
          <input className="pinput" type="number" min="0" max="7" value={form.activity} onChange={set('activity')} required />
        </label>
        {error && <p className="error-text">{error}</p>}
        {saved && <p className="ok-text">PROFILE SAVED</p>}
        <div className="row2">
          <button type="submit" className="pbtn" disabled={loading}>
            {loading ? '...' : 'SAVE PROFILE'}
          </button>
          <Link to="/targets" className="pbtn pbtn-ghost">
            TO GOALS
          </Link>
        </div>
      </form>
    </div>
  )
}
