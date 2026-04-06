import { useEffect, useState } from 'react'
import api from '../services/api'
import {
  RadialBarChart, RadialBar, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, Tooltip, Cell,
} from 'recharts'
import { MdLocalFireDepartment, MdWarning } from 'react-icons/md'

export default function Progress() {
  const [data, setData] = useState(null)

  useEffect(() => {
    api.get('/progress/progress').then((r) => setData(r.data)).catch(() => {})
  }, [])

  if (!data) return <div className="text-gray-500 text-sm">Loading progress...</div>

  const readinessData = Object.entries(data.exam_readiness || {}).map(([name, value]) => ({ name, value }))

  const getColor = (v) => v >= 70 ? '#22c55e' : v >= 40 ? '#f59e0b' : '#ef4444'

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Progress Analytics</h1>

      {/* Top stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard label="Total Tasks" value={data.total_tasks} />
        <StatCard label="Completed" value={data.completed_tasks} color="text-green-400" />
        <StatCard label="Completion Rate" value={`${data.completion_rate}%`} color="text-primary" />
        <StatCard label="Streak" value={`${data.streak} 🔥`} color="text-orange-400" />
      </div>

      {/* Weak alerts */}
      {data.weak_alerts?.length > 0 && (
        <div className="card border-red-800/50 bg-red-950/20">
          <div className="flex items-center gap-2 text-red-400 font-medium mb-2">
            <MdWarning /> Subjects below 40% completion
          </div>
          <div className="flex flex-wrap gap-2">
            {data.weak_alerts.map((s) => <span key={s} className="badge-weak">{s}</span>)}
          </div>
        </div>
      )}

      {/* Exam readiness chart */}
      {readinessData.length > 0 && (
        <div className="card">
          <h2 className="font-semibold mb-4">Exam Readiness by Subject</h2>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={readinessData} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
              <XAxis dataKey="name" tick={{ fill: '#9ca3af', fontSize: 12 }} />
              <YAxis domain={[0, 100]} tick={{ fill: '#9ca3af', fontSize: 12 }} />
              <Tooltip
                contentStyle={{ background: '#111827', border: '1px solid #374151', borderRadius: 8 }}
                formatter={(v) => [`${v}%`, 'Readiness']}
              />
              <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                {readinessData.map((entry, i) => (
                  <Cell key={i} fill={getColor(entry.value)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Completion donut */}
      <div className="card">
        <h2 className="font-semibold mb-4">Overall Completion</h2>
        <div className="flex items-center gap-6">
          <ResponsiveContainer width={160} height={160}>
            <RadialBarChart innerRadius="60%" outerRadius="100%" data={[{ value: data.completion_rate }]} startAngle={90} endAngle={-270}>
              <RadialBar dataKey="value" fill="#6366f1" background={{ fill: '#1f2937' }} cornerRadius={8} />
            </RadialBarChart>
          </ResponsiveContainer>
          <div>
            <div className="text-4xl font-bold text-primary">{data.completion_rate}%</div>
            <div className="text-sm text-gray-400 mt-1">{data.completed_tasks} of {data.total_tasks} tasks done</div>
            <div className="flex items-center gap-1 text-orange-400 mt-2">
              <MdLocalFireDepartment /> <span className="font-semibold">{data.streak} day streak</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function StatCard({ label, value, color = 'text-white' }) {
  return (
    <div className="card">
      <div className="text-xs text-gray-500 mb-1">{label}</div>
      <div className={`text-2xl font-bold ${color}`}>{value}</div>
    </div>
  )
}
