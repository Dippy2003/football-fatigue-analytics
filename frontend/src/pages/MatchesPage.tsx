import { useQuery } from '@tanstack/react-query'
import { ArrowRight } from 'lucide-react'
import { Link } from 'react-router-dom'

import { EmptyState, ErrorState, LoadingState } from '../components/ui/AsyncState'
import { StatusBadge } from '../components/ui/StatusBadge'
import { getMatches } from '../services/api/matches'

export function MatchesPage() {
  const query = useQuery({
    queryKey: ['matches'],
    queryFn: ({ signal }) => getMatches(signal),
  })
  if (query.isPending) return <LoadingState label="Loading matches" />
  if (query.isError) return <ErrorState retry={() => void query.refetch()} />
  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <p className="eyebrow">Explore</p>
          <h1>Matches</h1>
          <p>Choose a processed match and inspect its players and quality.</p>
        </div>
      </header>
      {query.data.length === 0 ? (
        <EmptyState message="No matches exist yet. Load the demo from the data page." />
      ) : (
        <div className="grid gap-4">
          {query.data.map((match) => (
            <Link className="match-card" key={match.id} to={`/matches/${match.id}`}>
              <div>
                <div className="flex gap-2">
                  <StatusBadge
                    label={match.is_synthetic ? 'Synthetic demo' : 'Local import'}
                    tone="info"
                  />
                  <StatusBadge label={match.processing_status} tone="success" />
                </div>
                <h2>{match.competition ?? 'Untitled match'}</h2>
                <p>{match.external_id}</p>
              </div>
              <ArrowRight aria-hidden="true" />
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
