const DEFAULT_API_BASE_URL = 'http://localhost:8000'

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  })

  if (!response.ok) {
    let message = 'Request failed'
    try {
      const data = await response.json()
      message = data?.detail || data?.message || message
    } catch {
      const text = await response.text()
      if (text) message = text
    }
    throw new Error(message)
  }

  return response.json()
}

export const catalogApi = {
  categorizeProduct(payload) {
    return request('/api/v1/catalog/categorize', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },
  listProducts() {
    return request('/api/v1/catalog/products')
  },
  getProduct(id) {
    return request(`/api/v1/catalog/products/${id}`)
  },
}

export const proposalsApi = {
  generateProposal(payload) {
    return request('/api/v1/proposals/generate', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },
  listProposals() {
    return request('/api/v1/proposals/')
  },
  getProposal(id) {
    return request(`/api/v1/proposals/${id}`)
  },
}

