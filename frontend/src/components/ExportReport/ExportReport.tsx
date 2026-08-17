import React from 'react';
import { Download, FileCheck, ShieldAlert } from 'lucide-react';
import { AnalysisResult } from '../../types/analysis';

interface ExportReportProps {
  result: AnalysisResult;
}

export const ExportReport: React.FC<ExportReportProps> = ({ result }) => {
  const handleExportPDF = () => {
    // Generate browser print / PDF download
    window.print();
  };

  return (
    <div style={{ margin: '1rem 0', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(19,27,46,0.6)', padding: '0.75rem 1.25rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
        <ShieldAlert size={16} color="#3b82f6" />
        <span>Báo cáo Rủi ro bao gồm {result.summary.riskyClauses} điều khoản cần lưu ý & Căn cứ Pháp lý Việt Nam</span>
      </div>

      <button className="btn-sample" onClick={handleExportPDF} style={{ background: 'linear-gradient(135deg, #3b82f6, #1d4ed8)', border: 'none', color: '#fff', fontWeight: 700 }}>
        <Download size={16} />
        <span>Xuất Báo Cáo PDF</span>
      </button>
    </div>
  );
};
