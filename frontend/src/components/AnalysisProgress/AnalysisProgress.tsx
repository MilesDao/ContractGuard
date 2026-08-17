import React from 'react';
import { Loader2, CheckCircle2, FileSearch, Cpu, Scale, ShieldCheck } from 'lucide-react';
import { AnalysisStep } from '../../types/analysis';

interface AnalysisProgressProps {
  step: AnalysisStep;
  fileName?: string;
}

export const AnalysisProgress: React.FC<AnalysisProgressProps> = ({ step, fileName }) => {
  const steps = [
    {
      id: 'PARSING',
      title: 'Đọc & Tách điều khoản văn bản',
      desc: 'Trích xuất văn bản hợp đồng bằng PyMuPDF',
      icon: FileSearch,
    },
    {
      id: 'CLASSIFYING',
      title: 'Phân loại rủi ro bằng PhoBERT',
      desc: 'Dự đoán 8 danh mục rủi ro theo luật Việt Nam',
      icon: Cpu,
    },
    {
      id: 'SCORING',
      title: 'Tính điểm mức độ nghiêm trọng (0-100)',
      desc: 'Đánh giá chỉ số rủi ro cho từng điều khoản',
      icon: Scale,
    },
    {
      id: 'SEARCHING_LAW',
      title: 'Truy xuất Căn cứ Pháp lý (FAISS RAG)',
      desc: 'Tìm kiếm Điều luật & đề xuất phương án sửa đổi',
      icon: ShieldCheck,
    },
  ];

  const getStepStatus = (stepId: string) => {
    const order = ['PARSING', 'CLASSIFYING', 'SCORING', 'SEARCHING_LAW', 'COMPLETED'];
    const currentIndex = order.indexOf(step);
    const stepIndex = order.indexOf(stepId);

    if (currentIndex > stepIndex) return 'completed';
    if (currentIndex === stepIndex) return 'active';
    return 'pending';
  };

  return (
    <div className="glass-panel progress-card">
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <Loader2 className="spin-icon" size={44} color="#3b82f6" style={{ margin: '0 auto 1rem' }} />
        <h3 style={{ fontSize: '1.35rem', fontWeight: 800 }}>Đang phân tích Hợp đồng...</h3>
        {fileName && (
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.3rem' }}>
            Tệp: <span style={{ color: '#60a5fa', fontFamily: 'var(--font-mono)' }}>{fileName}</span>
          </p>
        )}
      </div>

      <div className="step-list">
        {steps.map((s) => {
          const status = getStepStatus(s.id);
          const Icon = s.icon;
          return (
            <div key={s.id} className={`step-item ${status}`}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                {status === 'completed' ? (
                  <CheckCircle2 size={22} color="#10b981" />
                ) : status === 'active' ? (
                  <Loader2 className="spin-icon" size={22} color="#3b82f6" />
                ) : (
                  <Icon size={22} color="#64748b" />
                )}
              </div>
              <div style={{ flex: 1 }}>
                <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: status === 'pending' ? 'var(--text-dim)' : 'var(--text-main)' }}>
                  {s.title}
                </h4>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{s.desc}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
