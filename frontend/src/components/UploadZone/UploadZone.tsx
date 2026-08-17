import React, { useRef, useState } from 'react';
import { UploadCloud, FileCheck, AlertCircle, PlayCircle } from 'lucide-react';

interface UploadZoneProps {
  onFileUpload: (file: File) => void;
  onSelectSample: () => void;
}

export const UploadZone: React.FC<UploadZoneProps> = ({ onFileUpload, onSelectSample }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileUpload(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onFileUpload(e.target.files[0]);
    }
  };

  return (
    <div className="hero-section">
      <h2 className="hero-title">
        Phát hiện rủi ro pháp lý hợp đồng trong <span>dưới 8 giây</span>
      </h2>
      <p className="hero-subtitle">
        Sử dụng mô hình PhoBERT fine-tuned kết hợp FAISS RAG truy xuất chính xác Điều luật Việt Nam (BLDS 2015, BLLĐ 2019, NĐ 13/2023).
      </p>

      <div
        className={`upload-dropzone ${isDragOver ? 'active' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".pdf,.docx"
          style={{ display: 'none' }}
        />
        <div className="upload-icon-wrapper">
          <UploadCloud size={38} />
        </div>
        <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '0.5rem' }}>
          Tải lên Hợp đồng (PDF hoặc DOCX)
        </h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
          Kéo thả tệp văn bản vào đây hoặc nhấp để chọn tệp từ máy tính (Tối đa 10 MB)
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '1.5rem', marginTop: '1.5rem', fontSize: '0.8rem', color: 'var(--text-dim)' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
            <FileCheck size={14} color="#10b981" /> Bảo mật bộ nhớ đệm
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
            <AlertCircle size={14} color="#60a5fa" /> Tự động xóa sau phân tích
          </span>
        </div>
      </div>

      <div className="sample-selector">
        <span className="sample-label">Hoặc thử ngay với dữ liệu mẫu:</span>
        <div className="sample-buttons">
          <button className="btn-sample" onClick={onSelectSample}>
            <PlayCircle size={16} color="#3b82f6" />
            <span>Thử Hợp đồng Lao động Mẫu (Chứa 4 rủi ro)</span>
          </button>
        </div>
      </div>
    </div>
  );
};
