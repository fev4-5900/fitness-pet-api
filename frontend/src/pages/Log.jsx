import { useCallback, useEffect, useState } from 'react'
import { api } from '../api'
import PixelIcon from '../components/PixelIcon'

const TABS = [
  { id: 'meals', label: 'MEALS', icon: 'fire' },
  { id: 'water', label: 'WATER', icon: 'water' },
  { id: 'steps', label: 'STEPS', icon: 'paw' },
  { id: 'sleep', label: 'SLEEP', icon: 'moon' },
]

export default function Log() {
  const [tab, setTab] = useState('meals')
  return (
    <div className="page">
      <h1 className="pixel-title">LOG TODAY</h1>
      <div className="tabs">
        {TABS.map((t) => (
          <button
            key={t.id}
            type="button"
            className={`tab ${tab === t.id ? 'active' : ''}`}
            onClick={() => setTab(t.id)}
          >
            <PixelIcon name={t.icon} size={20} />
            <span>{t.label}</span>
          </button>
        ))}
      </div>
      {tab === 'meals' && <MealsSection />}
      {tab === 'water' && <WaterSection />}
      {tab === 'steps' && <StepsSection />}
      {tab === 'sleep' && <SleepSection />}
    </div>
  )
}

function Section({ title, children, total }) {
  return (
    <div className="panel stack">
      <div className="panel-head">
        <PixelIcon name="plus" size={20} />
        <h2 className="pixel-title small">{title}</h2>
        {total !== undefined && <span className="total-chip">{total}</span>}
      </div>
      {children}
    </div>
  )
}

function HistoryList({ items, onDelete, render }) {
  if (!items || items.length === 0) return <p className="muted">nothing logged yet today</p>
  return (
    <ul className="history">
      {items.map((it) => (
    <li key={it.id} className="history-row">
      <div className="history-main">{render(it)}</div>
      <button type="button" className="icon-btn" onClick={() => onDelete(it.id)} title="delete">
        <PixelIcon name="x" size={16} />
      </button>
    </li>
      ))}
    </ul>
  )
}

const MEAL_EMPTY = { calories: '', proteins: '', carbs: '', fats: '' }

function MealsSection() {
  const [form, setForm] = useState(MEAL_EMPTY)
  const [meals, setMeals] = useState([])
  const [totals, setTotals] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const refresh = useCallback(async () => {
    const [m, t] = await Promise.all([api.getTodayMeals(), api.getMealTotals()])
    setMeals(m)
    setTotals(t)
  }, [])

  useEffect(() => {
    refresh().catch(() => {})
  }, [refresh])

  function set(name) {
    return (e) => setForm((f) => ({ ...f, [name]: e.target.value }))
  }

  async function submit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await api.logMeal({
        calories: parseInt(form.calories, 10) || 0,
        proteins: parseInt(form.proteins, 10) || 0,
        carbs: parseInt(form.carbs, 10) || 0,
        fats: parseInt(form.fats, 10) || 0,
      })
      setForm(MEAL_EMPTY)
      await refresh()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function del(id) {
    await api.deleteMeal(id).catch(() => {})
    await refresh()
  }

  return (
    <Section
      title="LOG A MEAL"
      total={
        totals
          ? `${totals.calories} kcal - protein ${totals.proteins}g - carbs ${totals.carbs}g - fats ${totals.fats}g`
          : ''
      }
    >
      <form onSubmit={submit} className="grid4">
        {[
          { k: 'calories', label: 'KCAL' },
          { k: 'proteins', label: 'PROTEIN G' },
          { k: 'carbs', label: 'CARBS G' },
          { k: 'fats', label: 'FATS G' },
        ].map((f) => (
          <label key={f.k} className="field">
            <span>{f.label}</span>
            <input className="pinput" type="number" min="0" value={form[f.k]} onChange={set(f.k)} required />
          </label>
        ))}
        {error && <p className="error-text full">{error}</p>}
        <button type="submit" className="pbtn" disabled={loading}>
          {loading ? '...' : 'ADD MEAL'}
        </button>
      </form>
      <HistoryList
        items={meals}
        onDelete={del}
        render={(m) => (
          <div className="macro-line">
            <span className="macro-kcal">{m.calories} KCAL</span>
            <span className="macro-chip">PROTEIN {m.proteins}g</span>
            <span className="macro-chip">CARBS {m.carbs}g</span>
            <span className="macro-chip">FATS {m.fats}g</span>
          </div>
        )}
      />
    </Section>
  )
}

function WaterSection() {
  const [custom, setCustom] = useState('')
  const [list, setList] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const refresh = useCallback(async () => {
    const [w, t] = await Promise.all([api.getTodayWater(), api.getWaterTotals()])
    setList(w)
    return t
  }, [])

  const [total, setTotal] = useState(0)

  useEffect(() => {
    refresh().then(setTotal).catch(() => {})
  }, [refresh])

  async function log(liters) {
    setError('')
    setLoading(true)
    try {
      await api.logWater({ liters })
      setCustom('')
      setTotal(await refresh())
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function del(id) {
    await api.deleteWater(id).catch(() => {})
    setTotal(await refresh())
  }

  return (
    <Section title="LOG WATER" total={total ? `${total} L` : ''}>
      <div className="row2">
        <button type="button" className="pbtn" onClick={() => log(0.25)} disabled={loading}>
          +0.25 L
        </button>
        <button type="button" className="pbtn" onClick={() => log(0.5)} disabled={loading}>
          +0.5 L
        </button>
      </div>
      <form
        onSubmit={(e) => {
          e.preventDefault()
          const v = parseFloat(custom)
          if (v > 0) log(v)
        }}
        className="row2"
      >
        <input
          className="pinput"
          type="number"
          step="0.1"
          min="0"
          placeholder="liters..."
          value={custom}
          onChange={(e) => setCustom(e.target.value)}
        />
        <button type="submit" className="pbtn" disabled={loading}>
          ADD
        </button>
      </form>
      {error && <p className="error-text">{error}</p>}
      <HistoryList items={list} onDelete={del} render={(w) => `${w.liters} L`} />
    </Section>
  )
}

function StepsSection() {
  const [custom, setCustom] = useState('')
  const [list, setList] = useState([])
  const [total, setTotal] = useState(0)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const refresh = useCallback(async () => {
    const [s, t] = await Promise.all([api.getTodaySteps(), api.getStepTotals()])
    setList(s)
    return t
  }, [])

  useEffect(() => {
    refresh().then(setTotal).catch(() => {})
  }, [refresh])

  async function log(steps) {
    setError('')
    setLoading(true)
    try {
      await api.logSteps({ steps })
      setCustom('')
      setTotal(await refresh())
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function del(id) {
    await api.deleteSteps(id).catch(() => {})
    setTotal(await refresh())
  }

  return (
    <Section title="LOG STEPS" total={total ? `${total.toLocaleString()} steps` : ''}>
      <div className="row2">
        <button type="button" className="pbtn" onClick={() => log(1000)} disabled={loading}>
          +1,000
        </button>
        <button type="button" className="pbtn" onClick={() => log(5000)} disabled={loading}>
          +5,000
        </button>
      </div>
      <form
        onSubmit={(e) => {
          e.preventDefault()
          const v = parseInt(custom, 10)
          if (v > 0) log(v)
        }}
        className="row2"
      >
        <input
          className="pinput"
          type="number"
          min="0"
          placeholder="steps..."
          value={custom}
          onChange={(e) => setCustom(e.target.value)}
        />
        <button type="submit" className="pbtn" disabled={loading}>
          ADD
        </button>
      </form>
      {error && <p className="error-text">{error}</p>}
      <HistoryList
        items={list}
        onDelete={del}
        render={(s) => `${s.steps.toLocaleString()} steps`}
      />
    </Section>
  )
}

function SleepSection() {
  const [custom, setCustom] = useState('')
  const [list, setList] = useState([])
  const [total, setTotal] = useState(0)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const refresh = useCallback(async () => {
    const [s, t] = await Promise.all([api.getTodaySleep(), api.getSleepTotals()])
    setList(s)
    return t
  }, [])

  useEffect(() => {
    refresh().then(setTotal).catch(() => {})
  }, [refresh])

  async function log(hours) {
    setError('')
    setLoading(true)
    try {
      await api.logSleep({ sleep_hours: hours })
      setCustom('')
      setTotal(await refresh())
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function del(id) {
    await api.deleteSleep(id).catch(() => {})
    setTotal(await refresh())
  }

  return (
    <Section title="LOG SLEEP" total={total ? `${total} h` : ''}>
      <div className="row2">
        <button type="button" className="pbtn" onClick={() => log(8)} disabled={loading}>
          8H
        </button>
        <button type="button" className="pbtn" onClick={() => log(7)} disabled={loading}>
          7H
        </button>
      </div>
      <form
        onSubmit={(e) => {
          e.preventDefault()
          const v = parseFloat(custom)
          if (v > 0) log(v)
        }}
        className="row2"
      >
        <input
          className="pinput"
          type="number"
          step="0.5"
          min="0"
          max="24"
          placeholder="hours..."
          value={custom}
          onChange={(e) => setCustom(e.target.value)}
        />
        <button type="submit" className="pbtn" disabled={loading}>
          ADD
        </button>
      </form>
      {error && <p className="error-text">{error}</p>}
      <HistoryList items={list} onDelete={del} render={(s) => `${s.sleep_hours} h`} />
    </Section>
  )
}
