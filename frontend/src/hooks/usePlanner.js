import { useCallback, useState } from 'react'
import { createPlan } from '../lib/api'

export function usePlanner() {
  const [plan, setPlan] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const run = useCallback(async (files, scenario) => {
    setLoading(true)
    setError('')
    try {
      const nextPlan = await createPlan(files, scenario)
      setPlan(nextPlan)
      return nextPlan
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Unable to generate the plan.')
      return null
    } finally {
      setLoading(false)
    }
  }, [])

  return { plan, loading, error, run, clearError: () => setError('') }
}
