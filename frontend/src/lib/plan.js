const SCENARIO_NAMES = {
  A: 'Fixed Capacity',
  B: 'Fixed Completion Dates',
  C: 'Balanced Operations',
}

function asNumber(value) {
  const number = Number(value)
  return Number.isFinite(number) ? number : 0
}

function buildSummary(accessRows, resultRows) {
  const activities = new Set(accessRows.map((row) => String(row.activity_id)))
  const accessIds = new Set()
  let duplicates = 0
  for (const row of accessRows) {
    const key = `${row.activity_id}\u0000${row.access_seq}`
    if (accessIds.has(key)) duplicates += 1
    accessIds.add(key)
  }
  const overruns = resultRows.map((row) => asNumber(row.overrun_days))
  return {
    activities: activities.size,
    access_allocations: accessRows.length,
    contracts_late: overruns.filter((days) => days > 0).length,
    total_overrun_days: overruns.reduce((total, days) => total + days, 0),
    eclo_accesses: accessRows.reduce((total, row) => total + asNumber(row.eclo), 0),
    final_week: Math.max(0, ...accessRows.map((row) => asNumber(row.week))),
    duplicate_access_ids: duplicates,
  }
}

function buildAssurance(summary, scenario) {
  const generated = summary.activities > 0
  const duplicateFree = summary.duplicate_access_ids === 0
  const ecloValid = scenario !== 'A' || summary.eclo_accesses === 0
  return [
    { key: 'schedule', label: 'Schedule', status: generated ? 'pass' : 'fail', message: generated ? 'Schedule generated successfully.' : 'The generated schedule is empty.' },
    { key: 'duplicates', label: 'Access identifiers', status: duplicateFree ? 'pass' : 'fail', message: duplicateFree ? 'No duplicate access identifiers detected.' : `${summary.duplicate_access_ids} duplicate access identifier(s) detected.` },
    { key: 'eclo', label: 'ECLO policy', status: ecloValid ? 'pass' : 'fail', message: ecloValid ? 'Early Closure / Late Opening status is normal.' : 'ECLO access detected under Fixed Capacity mode.' },
  ]
}

function buildCapacity(rows) {
  const locationWeeks = new Map()
  for (const row of rows) {
    const location = String(row.location_id)
    const week = asNumber(row.week)
    const key = `${location}\u0000${week}`
    if (!locationWeeks.has(key)) {
      locationWeeks.set(key, { location_id: location, week, activities: new Set(), possessions: new Set() })
    }
    const entry = locationWeeks.get(key)
    entry.activities.add(String(row.activity_id))
    entry.possessions.add(String(row.co_share_group))
  }

  const locations = new Map()
  for (const entry of locationWeeks.values()) {
    if (!locations.has(entry.location_id)) locations.set(entry.location_id, [])
    locations.get(entry.location_id).push({
      week: entry.week,
      activities: entry.activities.size,
      possessions: entry.possessions.size,
    })
  }

  const locationSeries = [...locations.entries()].map(([location_id, weeks]) => ({
    location_id,
    weeks: weeks.sort((left, right) => left.week - right.week),
  }))
  const summary = locationSeries.map(({ location_id, weeks }) => ({
    location_id,
    total_possessions: weeks.reduce((total, week) => total + week.possessions, 0),
    total_activities: weeks.reduce((total, week) => total + week.activities, 0),
    active_weeks: weeks.length,
    peak_weekly_possessions: Math.max(0, ...weeks.map((week) => week.possessions)),
  })).sort((left, right) => right.total_possessions - left.total_possessions)

  return { summary, locations: locationSeries }
}

export function assemblePlan(datasets, scenario) {
  const summary = buildSummary(datasets.access.rows, datasets.results.rows)
  return {
    scenario,
    scenario_name: SCENARIO_NAMES[scenario],
    summary,
    assurance: buildAssurance(summary, scenario),
    datasets,
    analytics: {
      activity_options: [...new Set(datasets.access.rows.map((row) => String(row.activity_id)))].sort(),
      capacity: buildCapacity(datasets.occupancy.rows),
    },
  }
}
