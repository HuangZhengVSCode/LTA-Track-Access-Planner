import { createBrowserPlan } from './browserPlanner'

const API_ROOT = import.meta.env.VITE_API_URL?.replace(/\/$/, '')

async function parseResponse(response) {
  const payload = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(payload.detail || 'The planning service returned an unexpected error.')
  }
  return payload
}

export async function createPlan(files, scenario) {
  if (!API_ROOT) return createBrowserPlan(files, scenario)

  const body = new FormData()
  body.append('scenario', scenario)
  files.forEach((file) => body.append('files', file))

  const response = await fetch(`${API_ROOT}/plans`, { method: 'POST', body })
  return parseResponse(response)
}

export async function getConfiguration() {
  if (!API_ROOT) throw new Error('Configuration is bundled with the browser application.')
  const response = await fetch(`${API_ROOT}/configuration`)
  return parseResponse(response)
}
