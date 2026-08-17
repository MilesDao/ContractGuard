import React, { useEffect, useRef } from 'react';
import { FileText, Eye, AlertTriangle } from 'lucide-react';
import { ClauseResult } from '../../types/analysis';

interface DocumentViewerProps {
  contractTitle: string;
  clauses: ClauseResult[];
  selectedClauseId: string | null;
  onSelectClause: (clauseId: string) => void;
}

export const DocumentViewer: React.FC<DocumentViewerProps> = ({
  contractTitle,
  clauses,
  selectedClauseId,
  onSelectClause,
}) => {
  const clauseRefs = useRef<{ [key: string]: HTMLDivElement | null }>({});

  useEffect(() => {
    if (selectedClauseId && clauseRefs.current[selectedClauseId]) {
      clauseRefs.current[selectedClauseId]?.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
      });
    }
  }, [selectedClauseId]);

  const getRiskClass = (severity: number) => {
    if (severity >= 70) return 'risk-critical';
    if (severity >= 40) return 'risk-warning';
    return '';
  };

  return (
    <div className="glass-panel document-viewer-panel">
      <div className="panel-header">
        <div className="panel-title">
          <FileText size={18} color="#3b82f6" />
          <span>{contractTitle}</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
          <Eye size={14} />
          <span>Chế độ Xem Hợp Đồng</span>
        </div>
      </div>

      <div className="document-content">
        {clauses.map((clause) => {
          const isSelected = selectedClauseId === clause.id;
          const riskClass = getRiskClass(clause.severity);

          return (
            <div
              key={clause.id}
              ref={(el) => (clauseRefs.current[clause.id] = el)}
              className={`clause-block ${riskClass} ${isSelected ? 'selected' : ''}`}
              onClick={() => onSelectClause(clause.id)}
            >
              <div className="clause-header">
                <span className="clause-num">{clause.clauseNumber}</span>
                {clause.severity >= 70 && (
                  <span style={{ display: 'flex', alignItems: 'center', gap: '0.2rem', color: '#ef4444', fontSize: '0.75rem', fontWeight: 700 }}>
                    <AlertTriangle size={12} /> Cảnh báo Rủi ro Cao ({clause.severity})
                  </span>
                )}
              </div>
              <div className="clause-title">{clause.title}</div>
              <p className="clause-text">{clause.text}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
