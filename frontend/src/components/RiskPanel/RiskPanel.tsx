import React, { useState } from 'react';
import { AlertCircle, Filter } from 'lucide-react';
import { AnalysisResult } from '../../types/analysis';
import { SeverityGauge } from '../SeverityGauge/SeverityGauge';
import { RiskCard } from '../RiskCard/RiskCard';

interface RiskPanelProps {
  result: AnalysisResult;
  selectedClauseId: string | null;
  onSelectClause: (clauseId: string) => void;
}

export const RiskPanel: React.FC<RiskPanelProps> = ({
  result,
  selectedClauseId,
  onSelectClause,
}) => {
  const [filter, setFilter] = useState<'ALL' | 'CRITICAL' | 'WARNING'>('ALL');

  const filteredClauses = result.clauses.filter((c) => {
    if (c.severity === 0) return false; // Show only clauses with detected risk
    if (filter === 'CRITICAL') return c.severity >= 70;
    if (filter === 'WARNING') return c.severity >= 40 && c.severity < 70;
    return true;
  });

  return (
    <div className="glass-panel risk-dashboard-panel">
      <SeverityGauge result={result} />

      <div style={{ padding: '0.75rem 1.25rem', borderBottom: '1px solid var(--border-subtle)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: 'rgba(15,23,42,0.6)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.9rem', fontWeight: 700 }}>
          <AlertCircle size={16} color="#3b82f6" />
          <span>Danh sách Rủi ro Phát hiện ({filteredClauses.length})</span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
          <Filter size={14} color="var(--text-muted)" />
          <button
            onClick={() => setFilter('ALL')}
            style={{
              background: filter === 'ALL' ? 'var(--primary)' : 'transparent',
              color: filter === 'ALL' ? '#fff' : 'var(--text-muted)',
              border: 'none',
              borderRadius: '4px',
              padding: '0.2rem 0.5rem',
              fontSize: '0.75rem',
              cursor: 'pointer',
            }}
          >
            Tất cả
          </button>
          <button
            onClick={() => setFilter('CRITICAL')}
            style={{
              background: filter === 'CRITICAL' ? 'var(--critical)' : 'transparent',
              color: filter === 'CRITICAL' ? '#fff' : 'var(--text-muted)',
              border: 'none',
              borderRadius: '4px',
              padding: '0.2rem 0.5rem',
              fontSize: '0.75rem',
              cursor: 'pointer',
            }}
          >
            Cao
          </button>
        </div>
      </div>

      <div className="risk-cards-scroll">
        {filteredClauses.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-muted)' }}>
            <p>Không có rủi ro nào ở bộ lọc này.</p>
          </div>
        ) : (
          filteredClauses.map((clause) => (
            <RiskCard
              key={clause.id}
              clause={clause}
              isSelected={selectedClauseId === clause.id}
              onSelect={() => onSelectClause(clause.id)}
            />
          ))
        )}
      </div>
    </div>
  );
};
