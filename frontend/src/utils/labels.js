export const SOURCE_LABELS = {
  SAP: 'SAP',
  UTILITY: 'Utility',
  TRAVEL: 'Travel',
}

export const SOURCE_COLORS = {
  SAP: 'bg-violet-500/20 text-violet-300 ring-violet-500/30',
  UTILITY: 'bg-amber-500/20 text-amber-300 ring-amber-500/30',
  TRAVEL: 'bg-cyan-500/20 text-cyan-300 ring-cyan-500/30',
}

export const STATUS_COLORS = {
  PENDING: 'bg-amber-500/20 text-amber-300 ring-amber-500/40',
  APPROVED: 'bg-emerald-500/20 text-emerald-300 ring-emerald-500/40',
  REJECTED: 'bg-red-500/20 text-red-300 ring-red-500/40',
}

export const SCOPE_COLORS = {
  SCOPE_1: 'bg-orange-500/20 text-orange-300',
  SCOPE_2: 'bg-sky-500/20 text-sky-300',
  SCOPE_3: 'bg-indigo-500/20 text-indigo-300',
}

export function scopeNumber(scope) {
  if (!scope) return '—'
  const m = scope.match(/SCOPE_(\d)/)
  return m ? m[1] : scope
}

export const FLAG_LABELS = {
  MISSING_FIELD: 'Missing Data',
  INVALID_UNIT: 'Unit Converted',
  SUSPICIOUS_VALUE: 'Outlier Detected',
}

export const FLAG_STYLES = {
  MISSING_FIELD: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
  INVALID_UNIT: 'bg-blue-500/15 text-blue-300 border-blue-500/30',
  SUSPICIOUS_VALUE: 'bg-red-500/15 text-red-300 border-red-500/30',
}
