import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'
import PixelIcon from '../components/PixelIcon'

const FIELDS = [
  { k: 'calories', label: 'CALORIES', type: 'number' },
  { k: 'proteins', label: 'PROTEINS (G)', type: 'number' },
  { k: 'carbs', label: 'CARBS (G)', type: 'number' },
  { k: 'fats', label: 'FATS (G)', type: 'number' },
  { k: 'sleep_hours', label: 'SLEEP (H)', type: 'number', step: '0.5' },
  { k: 'steps', label: 'STEPS', type: 'number' },
  { k: 'water', label: 'WATER (L)', type: 'number', step: '0.1' },
]

export default function Targets() {
  const [form, setForm] = useState({})
  const [recommended, setRecommended] = useState(null)
  const [noProfile, setNoProfile] = useState(false)
  const [error, setError] = useState('')
  const [saved, setSaved] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    ;(async () => {
      try {
        const profile = await api.getProfile()
        if (!profile || !profile.gender || !profile.weight) {
          setNoProfile(true)
          return
        }
        const [rec, savedT] = await Promise.all([api.getRecommended(), api.getTargets()])
        setRecommended(rec)
        const base = savedT[0] || rec
        const f = {}
        FIELDS.forEach(({ k }) => (f[k] = base[k] ?? ''))
        setForm(f)
      } catch (err) {
        if (/profile|not found/i.test(err.message)) setNoProfile(true)
        else setError(err.message)
      } finally {
        setLoading(false)
      }
    })()
  }, [])

  function set(k) {
    return (e) => setForm((f) => ({ ...f, [k]: e.target.value }))
  }

  async function submit(e) {
    e.preventDefault()
    setError('')
    setSaved(false)
    try {
      const payload = {}
      FIELDS.forEach(({ k }) => (payload[k] = parseFloat(form[k]) || 0))
      await api.saveTargets(payload)
      setSaved(true)
    } catch (err) {
      setError(err.message)
    }
  }

  if (noProfile) {
    return (
      <div className="page">
        <h1 className="pixel-title">YOUR GOALS</h1>
        <div className="panel stack maxw">
          <p className="sub">
            COMPLETE YOUR PROFILE FIRST - the goal calculator needs your height, weight, age and
            gender to recommend targets.
          </p>
          <Link to="/profile" className="pbtn">
            SET UP PROFILE
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="page">
      <h1 className="pixel-title">DAILY GOALS</h1>
      <p className="sub">tune the numbers, save when happy</p>
      {recommended && (
        <div className="panel rec">
          <div className="panel-head">
            <PixelIcon name="star" size={20} />
            <h2 className="pixel-title small">RECOMMENDED FOR YOU</h2>
          </div>
          <div className="chips">
            {FIELDS.map(({ k, label }) => (
              <span key={k} className="chip">
                {label}: {recommended[k]}
              </span>
            ))}
          </div>
        </div>
      )}
      <form onSubmit={submit} className="panel stack maxw">
        <div className="grid2">
          {FIELDS.map(({ k, label, step }) => (
            <label key={k} className="field">
              <span>{label}</span>
              <input
                className="pinput"
                type="number"
                step={step || '1'}
                min="0"
                value={form[k] ?? ''}
                onChange={set(k)}
                required
              />
            </label>
          ))}
        </div>
        {error && <p className="error-text">{error}</p>}
        {saved && <p className="ok-text">GOALS SAVED</p>}
        <button type="submit" className="pbtn" disabled={loading}>
          {loading ? '...' : 'SAVE GOALS'}
        </button>
      </form>
    </div>
  )
}
