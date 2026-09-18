import { useMemo, useState } from 'react'
import { ChevronLeft, ChevronRight, Search } from 'lucide-react'

const PAGE_SIZE = 12

export default function DataTable({ dataset, emptyMessage = 'No records available.' }) {
  const [query, setQuery] = useState('')
  const [page, setPage] = useState(0)
  const rows = dataset?.rows || []
  const columns = dataset?.columns || []

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase()
    if (!needle) return rows
    return rows.filter((row) => columns.some((column) => String(row[column] ?? '').toLowerCase().includes(needle)))
  }, [columns, query, rows])

  const pages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE))
  const safePage = Math.min(page, pages - 1)
  const visible = filtered.slice(safePage * PAGE_SIZE, (safePage + 1) * PAGE_SIZE)

  return (
    <div className="table-shell">
      <div className="table-tools">
        <label className="search-field">
          <Search size={16} />
          <input
            value={query}
            onChange={(event) => { setQuery(event.target.value); setPage(0) }}
            placeholder="Search this dataset"
            aria-label="Search this dataset"
          />
        </label>
        <span>{filtered.length.toLocaleString()} records</span>
      </div>
      <div className="table-scroll">
        <table>
          <thead><tr>{columns.map((column) => <th key={column}>{column.replaceAll('_', ' ')}</th>)}</tr></thead>
          <tbody>
            {visible.map((row, index) => (
              <tr key={`${safePage}-${index}`}>
                {columns.map((column) => <td key={column}>{row[column] == null ? '—' : String(row[column])}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
        {!visible.length && <div className="empty-row">{emptyMessage}</div>}
      </div>
      <div className="pagination">
        <span>Page {safePage + 1} of {pages}</span>
        <div>
          <button className="icon-button" onClick={() => setPage(Math.max(0, safePage - 1))} disabled={safePage === 0} aria-label="Previous page"><ChevronLeft size={17} /></button>
          <button className="icon-button" onClick={() => setPage(Math.min(pages - 1, safePage + 1))} disabled={safePage >= pages - 1} aria-label="Next page"><ChevronRight size={17} /></button>
        </div>
      </div>
    </div>
  )
}
