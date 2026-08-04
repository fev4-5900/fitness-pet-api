import { useCallback, useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api, levelInfo } from '../api'
import Chinchilla from '../components/Chinchilla'
import Scene from '../components/Scene'
import PixelIcon from '../components/PixelIcon'
import ProgressBar from '../components/ProgressBar'

const MOOD_WORD = { happy: 'HAPPY', ok: 'CHILL', sad: 'SAD' }
const MOOD_COLOR = { happy: '#4E7A44', ok: '#B4824A', sad: '#A63D2F' }

export default function Dashboard() {
  const navigate = useNavigate()
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  const load = useCallback(async () => {
    const [pets, daily, total, targets, meals, water, sleep, steps, profile] = await Promise.all([
      api.getPets(),
      api.getDaily(),
      api.getTotal(),
      api.getTargets(),
      api.getMealTotals(),
      api.getWaterTotals(),
      api.getSleepTotals(),
      api.getStepTotals(),
      api.getProfile(),
    ])
    setData({
      pet: pets[0] || null,
      daily,
      total,
      targets: targets[0] || null,
      meals,
      water,
      sleep,
      steps,
      hasProfile: !!(profile && profile.gender && profile.weight),
    })
  }, [])

  useEffect(() => {
    load().catch((err) => {
      if (/credentials|unauthorized/i.test(err.message)) navigate('/login')
      else setError(err.message)
    })
  }, [load, navigate])

  if (!data) {
    return (
      <div className="page">
        <p className="loading">LOADING...</p>
        {error && <p className="error-text">{error}</p>}
      </div>
    )
  }

  const { pet, daily, total, targets, meals, water, sleep, steps, hasProfile } = data
  const level = levelInfo(total.total_points || 0)
  const mood = daily.effect || 'ok'
  const setup = []
  if (!hasProfile) setup.push({ to: '/profile', text: 'SET UP YOUR PROFILE' })
  if (!targets) setup.push({ to: '/targets', text: 'SET YOUR GOALS' })
  if (!pet) setup.push({ to: '/create-pet', text: 'ADOPT A CHINCHILLA' })

  const bars = [
    { label: 'CALORIES', icon: 'fire', value: meals?.calories || 0, max: targets?.calories, color: '#C75B22' },
    { label: 'PROTEIN', icon: 'meat', value: meals?.proteins || 0, max: targets?.proteins, color: '#A63D2F' },
    { label: 'WATER', icon: 'water', value: water?.liters || 0, max: targets?.water, color: '#33527A' },
    { label: 'SLEEP', icon: 'moon', value: sleep?.sleep_hours || 0, max: targets?.sleep_hours, color: '#6E4523' },
    { label: 'STEPS', icon: 'paw', value: steps?.steps || 0, max: targets?.steps, color: '#4E7A44' },
  ]

  return (
    <div className="page">
      {setup.length > 0 && (
        <div className="panel banner">
          <PixelIcon name="star" size={24} />
          <div>
            <strong>GET STARTED:</strong>
            <div className="banner-links">
              {setup.map((s) => (
                <Link key={s.to} to={s.to} className="plink">
                  {s.text}
                </Link>
              ))}
            </div>
          </div>
        </div>
      )}
      {error && <p className="error-text">{error}</p>}

      <div className="dash-grid">
        <div className="panel pet-card">
          <Scene>
            <Chinchilla mood={mood} level={level.level} size={210} />
          </Scene>
          <div className="pet-meta">
            <h2 className="pixel-title small">{pet?.name || 'CHINCHILLA'}</h2>
            <span className="level-badge">LV {level.level}</span>
          </div>
          <p className="mood-text" style={{ color: MOOD_COLOR[mood] }}>
            TODAY: {MOOD_WORD[mood]}
          </p>
          <div className="big-points">
            <span className="big-num">{daily.points}</span>
            <span className="big-lbl">/ 100</span>
          </div>
        </div>

        <div className="dash-side">
          <div className="panel">
            <div className="panel-head">
              <PixelIcon name="target" size={22} />
              <h2 className="pixel-title small">TODAY'S TARGETS</h2>
            </div>
            <div className="bars">
              {bars.map((b) => (
                <div key={b.label} className="bar-row">
                  <PixelIcon name={b.icon} size={22} />
                  <div className="bar-main">
                    <div className="bar-label">
                      <span>{b.label}</span>
                    </div>
                    <ProgressBar value={b.value} max={b.max || 0} color={b.color} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="panel">
            <div className="panel-head">
              <PixelIcon name="star" size={22} />
              <h2 className="pixel-title small">TOTAL POINTS</h2>
            </div>
            <div className="total-line">
              <span className="big-num">{total.total_points || 0}</span>
              {level.next && <span className="big-lbl"> / NEXT LV {level.next}</span>}
            </div>
            <ProgressBar value={total.total_points || 0} max={level.next || 0} color="#B4824A" />
            <div className="row2 quick">
              <Link to="/log" className="pbtn">
                LOG TODAY
              </Link>
              <Link to="/targets" className="pbtn pbtn-ghost">
                GOALS
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
