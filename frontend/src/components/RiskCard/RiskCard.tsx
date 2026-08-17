import React from 'react';
import { Scale, Sparkles, AlertTriangle, ArrowRight } from 'lucide-react';
import { ClauseResult } from '../../types/analysis';

interface RiskCardProps {
  clause: ClauseResult;
  isSelected: boolean;
  onSelect: () => void;
}

export const RiskCard: React.FC<RiskCardProps> = ({ clause, isSelected, onSelect }) => {
  const isCritical = clause.severity >= 70;
  const isWarning = clause.severity >= 40 && clause.severity < 70;

  const cardClass = isCritical ? 'risk-card-critical' : isWarning ? 'risk-card-warning' : '';

  return (
    <div
      className={`risk-card ${cardClass} ${isSelected ? 'selected' : ''}`}
      onClick={onSelect}
      style={{
        border: isSelected ? '1px solid var(--primary)' : undefined,
        background: isSelected ? '#19233c' : undefined,
        cursor: 'pointer',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ fontWeight: 800, fontSize: '0.9rem', color: isCritical ? '#ef4444' : isWarning ? '#f59e0b' : '#10b981' }}>
          {clause.clauseNumber} • {clause.title}
        </span>
        <span
          style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.8rem',
            fontWeight: 700,
            padding: '0.15rem 0.4rem',
            borderRadius: '4px',
            background: isCritical ? 'var(--critical-bg)' : 'var(--warning-bg)',
            color: isCritical ? '#fca5a5' : '#fde68a',
          }}
        >
          Điểm rủi ro: {clause.severity}/100
        </span>
      </div>

      <div className="risk-badges">
        {clause.labels.map((lbl) => (
          <span key={lbl} className={`badge-risk ${isCritical ? 'badge-risk-critical' : 'badge-risk-warning'}`}>
            {lbl}
          </span>
        ))}
      </div>

      <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: 1.5, marginBottom: '0.75rem' }}>
        {clause.explanation}
      </p>

      {clause.legalCitation && (
        <div className="legal-box">
          <div className="legal-title">
            <Scale size={14} />
            <span>Căn cứ Pháp lý Việt Nam:</span>
          </div>
          <p style={{ color: '#cbd5e1' }}>{clause.legalCitation}</p>
        </div>
      )}

      {clause.recommendation && (
        <div className="recommendation-box">
          <div className="recommendation-title" style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
            <Sparkles size={14} color="#10b981" />
            <span>Đề xuất Sửa đổi Pháp lý:</span>
          </div>
          <p style={{ color: '#e2e8f0' }}>{clause.recommendation}</p>
        </div>
      )}

      <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '0.75rem' }}>
        <span style={{ fontSize: '0.75rem', color: '#60a5fa', display: 'flex', alignItems: 'center', gap: '0.2rem', fontWeight: 600 }}>
          Xem vị trí trong văn bản <ArrowRight size={12} />
        </span>
      </div>
    </div>
  );
};
