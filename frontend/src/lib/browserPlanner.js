import SchedulerWorker from '../workers/scheduler.worker.js?worker'
import { assemblePlan } from './plan'

let worker
let requestSequence = 0
const pending = new Map()

function getWorker() {
  if (!worker) {
    worker = new SchedulerWorker()
    worker.onmessage = ({ data }) => {
      const request = pending.get(data.id)
      if (!request) return
      pending.delete(data.id)
      if (data.error) request.reject(new Error(data.error))
      else request.resolve(data.result)
    }
    worker.onerror = (event) => {
      for (const request of pending.values()) {
        request.reject(new Error(event.message || 'The browser scheduling engine stopped unexpectedly.'))
      }
      pending.clear()
      worker.terminate()
      worker = undefined
    }
  }
  return worker
}

export async function createBrowserPlan(files, scenario) {
  const payload = await Promise.all(
    files.map(async (file) => ({ name: file.name, content: await file.text() })),
  )
  const id = ++requestSequence
  const resultPromise = new Promise((resolve, reject) => pending.set(id, { resolve, reject }))
  getWorker().postMessage({ id, scenario, files: payload })
  const datasets = await resultPromise
  return assemblePlan(datasets, scenario)
}
