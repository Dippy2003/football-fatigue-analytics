export const RISK_DISCLAIMER =
  'PlayerPulse provides performance-based indicators from available match data. It is not a medical diagnostic tool and must not be used as a substitute for qualified medical or sports-science assessment.'

export type DemoDataset = {
  dataset_import_id: string
  match_id: string
  player_count: number
  is_synthetic: boolean
  created: boolean
}

export type DataSource = {
  id: string
  provider: string
  usage_status: string
  attribution: string
}

export type Match = {
  id: string
  external_id: string
  competition: string | null
  home_team_id: string
  away_team_id: string
  is_synthetic: boolean
  processing_status: string
}

export type MatchPlayer = {
  id: string
  external_id: string
  name: string
  position: string | null
  team_id: string
  total_distance_m: number
  data_quality_score: number
}

export type TeamSummary = {
  team_id: string
  team_name: string
  player_count: number
  total_distance_m: number
  sprint_count: number
}

export type MatchQuality = {
  match_id: string
  data_quality_score: number
  player_metric_coverage: number
  limitations: string[]
}

export type PlayerProfile = {
  id: string
  external_id: string
  name: string
  position: string | null
  team_id: string
  source: string
}

export type PlayerMetrics = {
  match_id: string
  player_id: string
  playing_minutes: number
  total_distance_m: number
  distance_per_minute: number
  average_speed_mps: number
  max_speed_mps: number
  high_speed_distance_m: number
  sprint_count: number
  sprint_distance_m: number
  median_sprint_recovery_seconds: number | null
  acceleration_count: number
  deceleration_count: number
  second_half_speed_change_pct: number | null
  late_match_sprint_change_pct: number | null
  late_match_distance_change_pct: number | null
  pass_accuracy_change_pct: number | null
  pressure_change_pct: number | null
  possession_loss_change: number | null
  workload_vs_baseline_zscore: number | null
  data_quality_score: number
  baseline_type: string | null
  baseline_confidence: number | null
  supported_event_metrics: boolean
  feature_version: string
}

export type TimelinePoint = {
  period: number
  timestamp_seconds: number
  x: number
  y: number
}

export type Timeline = {
  downsampled: boolean
  point_count: number
  points: TimelinePoint[]
}

export type Heatmap = {
  rows: number
  columns: number
  max_count: number
  grid: number[][]
}

export type PlayerEvents = {
  supported: boolean
  events: Array<Record<string, unknown>>
}

export type Baseline = {
  baseline_type: string
  baseline_confidence: number
  workload_zscore: number | null
  sample_size: number
  limitation: string
}

export type RiskFactor = {
  name: string
  raw_value: number
  normalized_value: number
  configured_weight: number
  effective_weight: number
  contribution: number
  explanation: string
}

export type RiskAssessment = {
  assessment_status: string
  score: number | null
  category: string | null
  confidence: number
  factors: RiskFactor[]
  explanation: string
  limitations: string[]
  disclaimer: string
  model_version: string
  calculated_at: string
}

export type ComparisonPlayer = {
  player_id: string
  name: string
  position: string | null
  total_distance_m: number
  max_speed_mps: number
  sprint_count: number
  data_quality_score: number
}

export type Comparison = {
  match_id: string
  players: ComparisonPlayer[]
  warning: string
}

export type ProcessingJob = {
  id?: string
  job_id?: string
  match_id?: string
  status: string
  stage: string
  progress?: number
  error_message?: string | null
  limitation?: string
}
