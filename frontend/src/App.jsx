import './App.css'
import { useState } from 'react'
import { catalogApi, proposalsApi } from './api.js'

function Nav({ current, onChange }) {
  return (
    <header className="app-header">
      <div className="app-brand">
        <span className="app-logo">♻️</span>
        <div>
          <h1>AI Sustainable Commerce</h1>
          <p>Catalog intelligence & B2B proposal generator</p>
        </div>
      </div>
      <nav className="app-nav">
        <button
          className={current === 'catalog' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => onChange('catalog')}
        >
          Catalog AI
        </button>
        <button
          className={current === 'proposals' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => onChange('proposals')}
        >
          B2B Proposals
        </button>
      </nav>
    </header>
  )
}

function CatalogPage() {
  const [form, setForm] = useState({ name: '', description: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    if (!form.name.trim() || !form.description.trim()) {
      setError('Please provide both a product name and description.')
      return
    }
    setLoading(true)
    try {
      const data = await catalogApi.categorizeProduct(form)
      setResult(data)
      setHistory((prev) => [data, ...prev])
    } catch (err) {
      setError(err.message || 'Something went wrong while categorizing.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <section className="panel">
        <h2>AI Auto-Category & Tag Generator</h2>
        <p className="panel-subtitle">
          Paste any sustainable product and instantly get categories, SEO tags, and filters.
        </p>
        <form className="form" onSubmit={handleSubmit}>
          <div className="field">
            <label>Product name</label>
            <input
              type="text"
              placeholder="e.g. Bamboo Toothbrush"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />
          </div>
          <div className="field">
            <label>Product description</label>
            <textarea
              rows="5"
              placeholder="Describe the materials, use, and sustainability aspects..."
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
            />
          </div>
          {error && <p className="error">{error}</p>}
          <button className="primary-btn" type="submit" disabled={loading}>
            {loading ? 'Thinking with Gemini…' : 'Categorize product'}
          </button>
        </form>
      </section>

      <section className="layout-two-columns">
        <div className="panel">
          <h3>AI Output</h3>
          {!result && <p className="muted">Run a categorization to see structured AI output.</p>}
          {result && (
            <div className="card">
              <h4>
                {result.primary_category} &raquo; {result.sub_category}
              </h4>
              <p className="muted">{result.description}</p>
              <div className="pill-group">
                {result.seo_tags.map((tag) => (
                  <span key={tag} className="pill">
                    {tag}
                  </span>
                ))}
              </div>
              {result.sustainability_filters.length > 0 && (
                <>
                  <h5>Sustainability filters</h5>
                  <div className="pill-group">
                    {result.sustainability_filters.map((f) => (
                      <span key={f} className="pill pill-green">
                        {f}
                      </span>
                    ))}
                  </div>
                </>
              )}
              <p className="meta">
                ID: {result.product_id} • Created at:{' '}
                {new Date(result.created_at).toLocaleString()}
              </p>
            </div>
          )}
        </div>

        <div className="panel">
          <h3>Recent runs (this session)</h3>
          {history.length === 0 && (
            <p className="muted">Your recent categorizations will appear here.</p>
          )}
          <ul className="history-list">
            {history.map((item) => (
              <li key={item.product_id} className="history-item">
                <div>
                  <strong>{item.name}</strong>
                  <span className="muted small">
                    {item.primary_category} &raquo; {item.sub_category}
                  </span>
                </div>
                <span className="small">
                  {new Date(item.created_at).toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </span>
              </li>
            ))}
          </ul>
        </div>
      </section>
    </div>
  )
}

function ProposalsPage() {
  const [form, setForm] = useState({
    company_name: '',
    industry: '',
    budget: '',
    preferencesText: '',
    quantity_needed: '',
    use_case: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [proposal, setProposal] = useState(null)
  const [history, setHistory] = useState([])

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    if (!form.company_name.trim() || !form.industry.trim() || !form.use_case.trim()) {
      setError('Company, industry, and use case are required.')
      return
    }
    const budget = Number(form.budget)
    const quantity = Number(form.quantity_needed)
    if (!Number.isFinite(budget) || budget <= 0 || !Number.isFinite(quantity) || quantity <= 0) {
      setError('Budget and quantity must be positive numbers.')
      return
    }
    const preferences =
      form.preferencesText
        .split(',')
        .map((p) => p.trim())
        .filter(Boolean) || []

    const payload = {
      company_name: form.company_name,
      industry: form.industry,
      budget,
      preferences,
      quantity_needed: quantity,
      use_case: form.use_case,
    }

    setLoading(true)
    try {
      const data = await proposalsApi.generateProposal(payload)
      setProposal(data)
      setHistory((prev) => [data, ...prev])
    } catch (err) {
      setError(err.message || 'Something went wrong while generating the proposal.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <section className="panel">
        <h2>AI B2B Proposal Generator</h2>
        <p className="panel-subtitle">
          Generate a full sustainable procurement proposal for your B2B client in one click.
        </p>
        <form className="form grid-two" onSubmit={handleSubmit}>
          <div className="field">
            <label>Company name</label>
            <input
              type="text"
              placeholder="e.g. GreenCorp Solutions"
              value={form.company_name}
              onChange={(e) => setForm({ ...form, company_name: e.target.value })}
            />
          </div>
          <div className="field">
            <label>Industry</label>
            <input
              type="text"
              placeholder="e.g. Corporate gifting"
              value={form.industry}
              onChange={(e) => setForm({ ...form, industry: e.target.value })}
            />
          </div>
          <div className="field">
            <label>Total budget (INR)</label>
            <input
              type="number"
              min="1"
              placeholder="e.g. 50000"
              value={form.budget}
              onChange={(e) => setForm({ ...form, budget: e.target.value })}
            />
          </div>
          <div className="field">
            <label>Total quantity needed</label>
            <input
              type="number"
              min="1"
              placeholder="e.g. 100"
              value={form.quantity_needed}
              onChange={(e) => setForm({ ...form, quantity_needed: e.target.value })}
            />
          </div>
          <div className="field">
            <label>Sustainability preferences (comma-separated)</label>
            <input
              type="text"
              placeholder="e.g. plastic-free, vegan, recycled"
              value={form.preferencesText}
              onChange={(e) => setForm({ ...form, preferencesText: e.target.value })}
            />
          </div>
          <div className="field full">
            <label>Use case</label>
            <textarea
              rows="3"
              placeholder="Describe the occasion, recipients, and context..."
              value={form.use_case}
              onChange={(e) => setForm({ ...form, use_case: e.target.value })}
            />
          </div>
          {error && (
            <div className="field full">
              <p className="error">{error}</p>
            </div>
          )}
          <div className="field full align-right">
            <button className="primary-btn" type="submit" disabled={loading}>
              {loading ? 'Drafting proposal…' : 'Generate proposal'}
            </button>
          </div>
        </form>
      </section>

      <section className="layout-two-columns">
        <div className="panel">
          <h3>Proposal overview</h3>
          {!proposal && (
            <p className="muted">Submit client details to generate a tailored proposal.</p>
          )}
          {proposal && (
            <div className="proposal">
              <div className="proposal-header">
                <h4>{proposal.company_name}</h4>
                <p className="muted">
                  {proposal.industry} • Budget ₹{proposal.total_budget.toLocaleString('en-IN')} •{' '}
                  {proposal.quantity_needed} units
                </p>
                <p className="small">
                  Created at {new Date(proposal.created_at).toLocaleString()}
                </p>
              </div>

              <div className="proposal-section">
                <h5>Product mix</h5>
                <ul className="product-mix">
                  {proposal.product_mix.map((item, index) => (
                    <li key={`${item.product_name}-${index}`} className="product-mix-item">
                      <div className="product-main">
                        <strong>{item.product_name}</strong>
                        <span className="muted small">
                          {item.category} • {item.quantity} units @ ₹
                          {item.unit_price.toLocaleString('en-IN')} =&nbsp;₹
                          {item.total_price.toLocaleString('en-IN')}
                        </span>
                      </div>
                      <div className="pill-group">
                        {item.sustainability_attributes.map((attr) => (
                          <span key={attr} className="pill pill-green">
                            {attr}
                          </span>
                        ))}
                      </div>
                      {item.reason && <p className="small">{item.reason}</p>}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="proposal-section grid-two">
                <div>
                  <h5>Budget allocation</h5>
                  <ul className="kv-list">
                    {Object.entries(proposal.budget_allocation).map(([label, value]) => (
                      <li key={label}>
                        <span>{label}</span>
                        <span>₹{Number(value).toLocaleString('en-IN')}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h5>Cost breakdown</h5>
                  <ul className="kv-list">
                    {Object.entries(proposal.estimated_cost_breakdown).map(([label, value]) => (
                      <li key={label}>
                        <span>{label}</span>
                        <span>₹{Number(value).toLocaleString('en-IN')}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="proposal-section">
                <h5>Impact summary</h5>
                <p>{proposal.impact_summary}</p>
              </div>
            </div>
          )}
        </div>

        <div className="panel">
          <h3>Recent proposals (this session)</h3>
          {history.length === 0 && (
            <p className="muted">Once generated, proposals will appear here for quick recall.</p>
          )}
          <ul className="history-list">
            {history.map((item) => (
              <li
                key={item.proposal_id}
                className="history-item clickable"
                onClick={() => setProposal(item)}
              >
                <div>
                  <strong>{item.company_name}</strong>
                  <span className="muted small">
                    {item.industry} • ₹{item.total_budget.toLocaleString('en-IN')}
                  </span>
                </div>
                <span className="small">
                  {new Date(item.created_at).toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </span>
              </li>
            ))}
          </ul>
        </div>
      </section>
    </div>
  )
}

function App() {
  const [page, setPage] = useState('catalog')

  return (
    <div className="app-shell">
      <Nav current={page} onChange={setPage} />
      <main className="app-main">
        {page === 'catalog' && <CatalogPage />}
        {page === 'proposals' && <ProposalsPage />}
      </main>
      <footer className="app-footer">
        <span>Backend: FastAPI · Google Gemini · SQLite</span>
      </footer>
    </div>
  )
}

export default App
