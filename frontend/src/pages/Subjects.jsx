import { useEffect, useState } from 'react'
import toast from 'react-hot-toast'
import api from '../services/api'
import { MdAdd, MdDelete, MdExpandMore, MdExpandLess } from 'react-icons/md'

const DEFAULTS = { name: '', code: '', exam_date: '', difficulty: 3, syllabus: '' }

const SYLLABUS_PRESETS = {
  DSA: `Arrays and Strings\nLinked Lists\nStacks and Queues\nTrees and Binary Search Trees\nGraphs - BFS and DFS\nDynamic Programming\nSorting Algorithms\nSearching Algorithms\nHashing\nGreedy Algorithms\nBacktracking\nDivide and Conquer`,
  DBMS: `ER Model and Relational Model\nSQL Basics - DDL and DML\nSQL Joins and Subqueries\nNormalization - 1NF 2NF 3NF BCNF\nTransaction Management and ACID\nConcurrency Control\nIndexing and Hashing\nQuery Optimization\nFile Organization\nNoSQL Databases`,
  OS: `Process Management and Scheduling\nThreads and Concurrency\nProcess Synchronization\nDeadlocks - Detection and Prevention\nMemory Management\nVirtual Memory and Paging\nFile System Interface\nDisk Scheduling\nI/O Systems\nSecurity and Protection`,
  CN: `OSI and TCP/IP Models\nPhysical Layer - Transmission Media\nData Link Layer - Framing and Error Control\nMAC Protocols\nNetwork Layer - IP Addressing\nRouting Algorithms\nTransport Layer - TCP and UDP\nApplication Layer - HTTP DNS FTP\nNetwork Security\nWireless Networks`,
  Maths: `Matrices and Determinants\nEigenvalues and Eigenvectors\nDifferential Calculus\nIntegral Calculus\nDifferential Equations\nLaplace Transforms\nFourier Series\nProbability Theory\nStatistics\nNumerical Methods`,
}

export default function Subjects() {
  const [subjects, setSubjects] = useState([])
  const [form, setForm] = useState(DEFAULTS)
  const [loading, setLoading] = useState(false)
  const [expanded, setExpanded] = useState(null)

  const fetchSubjects = () => api.get('/subjects').then((r) => setSubjects(r.data))
  useEffect(() => { fetchSubjects() }, [])

  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }))

  const applyPreset = (name) => {
    const preset = SYLLABUS_PRESETS[name]
    if (preset) set('syllabus', preset)
  }

  const handleAdd = async (e) => {
    e.preventDefault()
    const syllabusArr = form.syllabus
      .split('\n')
      .map((t) => t.trim())
      .filter(Boolean)

    if (syllabusArr.length === 0) {
      toast.error('Add at least one syllabus topic')
      return
    }

    setLoading(true)
    try {
      await api.post('/subjects', {
        name: form.name,
        code: form.code,
        exam_date: form.exam_date || null,
        difficulty: +form.difficulty,
        syllabus: syllabusArr,
      })
      toast.success(`Subject added with ${syllabusArr.length} topics`)
      setForm(DEFAULTS)
      fetchSubjects()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to add subject')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    await api.delete(`/subjects/${id}`)
    toast.success('Removed')
    fetchSubjects()
  }

  const difficultyLabel = (d) => ['', 'Very Easy', 'Easy', 'Medium', 'Hard', 'Very Hard'][+d]

  return (
    <div className="space-y-6 max-w-3xl">
      <h1 className="text-2xl font-bold">Subjects & Syllabus</h1>

      {/* Add form */}
      <div className="card">
        <h2 className="font-semibold mb-4">Add Subject</h2>
        <form onSubmit={handleAdd} className="space-y-4">

          {/* Row 1 */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-gray-400 mb-1 block">Subject Name *</label>
              <input className="input" required placeholder="e.g. DSA" value={form.name}
                onChange={(e) => set('name', e.target.value)} />
            </div>
            <div>
              <label className="text-xs text-gray-400 mb-1 block">Subject Code</label>
              <input className="input" placeholder="CS301" value={form.code}
                onChange={(e) => set('code', e.target.value)} />
            </div>
          </div>

          {/* Row 2 */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-gray-400 mb-1 block">Exam Date</label>
              <input className="input" type="date" value={form.exam_date}
                onChange={(e) => set('exam_date', e.target.value)} />
            </div>
            <div>
              <label className="text-xs text-gray-400 mb-1 block">
                Difficulty: <span className="text-primary">{difficultyLabel(form.difficulty)}</span>
              </label>
              <input type="range" min="1" max="5" className="w-full accent-primary mt-2"
                value={form.difficulty} onChange={(e) => set('difficulty', e.target.value)} />
            </div>
          </div>

          {/* Syllabus */}
          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="text-xs text-gray-400">Syllabus Topics * (one per line)</label>
              <div className="flex gap-1 flex-wrap justify-end">
                {Object.keys(SYLLABUS_PRESETS).map((name) => (
                  <button key={name} type="button"
                    onClick={() => { set('name', name); applyPreset(name) }}
                    className="text-xs px-2 py-0.5 bg-gray-700 hover:bg-primary/30 text-gray-300 rounded transition-colors">
                    {name}
                  </button>
                ))}
              </div>
            </div>
            <textarea
              className="input min-h-[160px] resize-y font-mono text-xs leading-relaxed"
              placeholder={`Arrays and Strings\nLinked Lists\nStacks and Queues\nTrees and BST\n...`}
              value={form.syllabus}
              onChange={(e) => set('syllabus', e.target.value)}
            />
            <p className="text-xs text-gray-600 mt-1">
              {form.syllabus.split('\n').filter(Boolean).length} topics entered
            </p>
          </div>

          <button className="btn-primary flex items-center gap-2" disabled={loading}>
            <MdAdd /> {loading ? 'Adding...' : 'Add Subject'}
          </button>
        </form>
      </div>

      {/* Subject list */}
      <div className="space-y-3">
        {subjects.length === 0 && (
          <p className="text-gray-500 text-sm">No subjects added yet. Add one above.</p>
        )}
        {subjects.map((s) => (
          <div key={s.id} className="card">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="font-medium">{s.name}</span>
                  {s.code && <span className="text-gray-500 text-xs">({s.code})</span>}
                  <span className={`text-xs px-2 py-0.5 rounded-full ${
                    s.difficulty >= 4 ? 'bg-red-900/40 text-red-400'
                    : s.difficulty === 3 ? 'bg-yellow-900/40 text-yellow-400'
                    : 'bg-green-900/40 text-green-400'
                  }`}>{difficultyLabel(s.difficulty)}</span>
                </div>
                <div className="text-xs text-gray-500 mt-0.5">
                  {s.syllabus?.length || 0} topics
                  {s.exam_date && ` · Exam: ${s.exam_date}`}
                </div>
              </div>
              <div className="flex items-center gap-2">
                <button onClick={() => setExpanded(expanded === s.id ? null : s.id)}
                  className="text-gray-500 hover:text-white transition-colors">
                  {expanded === s.id ? <MdExpandLess className="text-lg" /> : <MdExpandMore className="text-lg" />}
                </button>
                <button onClick={() => handleDelete(s.id)}
                  className="text-gray-600 hover:text-red-400 transition-colors">
                  <MdDelete className="text-lg" />
                </button>
              </div>
            </div>

            {/* Expanded syllabus */}
            {expanded === s.id && s.syllabus?.length > 0 && (
              <div className="mt-3 pt-3 border-t border-gray-800">
                <p className="text-xs text-gray-500 mb-2">Syllabus ({s.syllabus.length} topics)</p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-1">
                  {s.syllabus.map((topic, i) => (
                    <div key={i} className="flex items-center gap-2 text-xs text-gray-300 bg-gray-800 px-2 py-1.5 rounded">
                      <span className="text-gray-600 w-5 text-right flex-shrink-0">{i + 1}.</span>
                      {topic}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
