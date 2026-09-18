const apiUrl = process.env.VITE_API_URL?.trim()

if (apiUrl) {
  let parsed
  try {
    parsed = new URL(apiUrl)
  } catch {
    console.error('VITE_API_URL must be a valid absolute URL.')
    process.exit(1)
  }

  if (process.env.NETLIFY === 'true' && parsed.protocol !== 'https:') {
    console.error('VITE_API_URL must use HTTPS for a Netlify production deployment.')
    process.exit(1)
  }

  if (!parsed.pathname.replace(/\/$/, '').endsWith('/api/v1')) {
    console.error('VITE_API_URL must end with /api/v1.')
    process.exit(1)
  }
}

console.log(`Deployment configuration valid (${apiUrl || 'in-browser Python engine'}).`)
