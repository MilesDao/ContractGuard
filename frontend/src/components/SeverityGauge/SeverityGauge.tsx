import React from 'react';
import { AlertTriangle, AlertCircle, CheckCircle } from 'lucide-react';
import { AnalysisResult } from '../../types/analysis';

interface SeverityGaugeProps {
  result: AnalysisResult;
}

export const SeverityGauge: React.FC<SeverityGaugeProps> = ({ result }) => {
  const { overallScore, statusGrade, summary } = result;

  const getStatusDetails = () => {
    if (overallScore >= 70) {
      return {
        label: 'RỦI RO CAO',
        color: '#ef4444',
        icon: AlertTriangle,
        desc: 'Hợp đồng chứa nhiều điều khoản bất lợi vi phạm pháp luật.',
      };
    }
    if (overallScore >= 40) {
      return {
        label: 'CẢNH BÁO',
        color: '#f59e0b',
        icon: AlertCircle,
        desc: 'Có điều khoản cần điều chỉnh lại trước khi ký.',
      };
    }
    return {
      label: 'AN TOÀN',
      color: '#10b981',
      icon: CheckCircle,
      desc: 'Hợp đồng đáp ứng các tiêu chuẩn pháp lý cơ bản.',
    };
  };

  const status = getStatusDetails();
  const StatusIcon = status.icon;

  // SVG Gauge calculations
  const strokeDasharray = 283;
  const strokeDashoffset = strokeDasharray - (strokeDasharray * overallScore) / 100;

  return (
    <div className="severity-gauge-wrapper">
      <div className="gauge-chart">
        <svg viewBox="0 0 100 100" style={{ transform: 'rotate(-90deg)', width: '100%', height: '100%' }}>
          <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth="8" />
          <circle
            cx="50"
            cy="50"
            r="45"
            fill="none"
            stroke={status.color}
            strokeWidth="8"
            strokeDasharray={strokeDasharray}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            style={{ transition: 'stroke-dashoffset 1s ease-in-out' }}
          />
        </svg>
        <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <span style={{ fontSize: '1.6rem', fontWeight: 800, color: status.color, lineHeight: 1 }}>{overallScore}</span>
          <span style={{ fontSize: '0.65rem', color: 'var(--text-dim)', textTransform: 'uppercase', marginTop: '2px' }}>/ 100</span>
        </div>
      </div>

      <div style={{ flex: 1 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.3rem' }}>
          <StatusIcon size={20} color={status.color} />
          <span style={{ fontWeight: 800, fontSize: '1.1rem', color: status.color }}>{status.label}</span>
        </div>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>{status.desc}</p>

        <div style={{ display: 'flex', gap: '0.75rem', fontSize: '0.75rem' }}>
          <span style={{ background: 'var(--critical-bg)', color: '#fca5a5', padding: '0.2rem 0.5rem', borderRadius: '4px', border: '1px solid var(--critical-border)' }}>
            Nghiêm trọng: {summary.criticalCount}
          </span>
          <span style={{ background: 'var(--warning-bg)', color: '#fde68a', padding: '0.2rem 0.5rem', borderRadius: '4px', border: '1px solid var(--warning-border)' }}>
            Trung bình: {summary.highCount + summary.mediumCount}
          </span>
        </div>
      </div>
    </div>
  );
};
