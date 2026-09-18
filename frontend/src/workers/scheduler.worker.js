const PYODIDE_ROOT = 'https://cdn.jsdelivr.net/pyodide/v314.0.7/full/'

let runtimePromise

async function getRuntime() {
  if (!runtimePromise) {
    runtimePromise = (async () => {
      const { loadPyodide } = await import(/* @vite-ignore */ `${PYODIDE_ROOT}pyodide.mjs`)
      const runtime = await loadPyodide({ indexURL: PYODIDE_ROOT })
      await runtime.loadPackage('pandas')
      const response = await fetch('/scheduler.py')
      if (!response.ok) throw new Error('The packaged scheduling engine could not be loaded.')
      const source = await response.text()
      runtime.globals.set('scheduler_source', source)
      await runtime.runPythonAsync(`
_scheduler_namespace = {}
exec(scheduler_source, _scheduler_namespace)
_run_scheduler = _scheduler_namespace["run_track_access_scheduler"]
`)
      return runtime
    })()
  }
  return runtimePromise
}

self.onmessage = async ({ data }) => {
  const { id, scenario, files } = data
  try {
    const runtime = await getRuntime()
    runtime.globals.set('uploaded_files_json', JSON.stringify(files))
    runtime.globals.set('selected_scenario', scenario)

    const result = await runtime.runPythonAsync(`
import io
import json

_uploaded_files = json.loads(uploaded_files_json)
_file_objects = {
    item["name"]: io.StringIO(item["content"])
    for item in _uploaded_files
}
_access, _occupancy, _results = _run_scheduler(
    _file_objects,
    scenario=selected_scenario,
)

def _dataset(frame):
    return {
        "columns": [str(column) for column in frame.columns],
        "rows": json.loads(frame.to_json(orient="records", date_format="iso")),
    }

json.dumps({
    "access": _dataset(_access),
    "occupancy": _dataset(_occupancy),
    "results": _dataset(_results),
})
`)
    self.postMessage({ id, result: JSON.parse(result) })
  } catch (reason) {
    self.postMessage({
      id,
      error: reason instanceof Error ? reason.message : String(reason),
    })
  }
}
