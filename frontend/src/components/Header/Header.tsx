import React from 'react';
import { Shield, ShieldAlert, FileText } from 'lucide-react';

interface HeaderProps {
  onReset?: () => void;
  hasResult?: boolean;
}

export const Header: React.FC<HeaderProps> = ({ onReset, hasResult }) => {
  return (
    <header className="header-bar">
      <div className="brand-zone" onClick={onReset} style={{ cursor: onReset ? 'pointer' : 'default' }}>
        <div className="brand-icon">
          <Shield size={22} color="#ffffff" />
        </div>
        <div>
          <h1 className="brand-title">ContractGuard</h1>
          <span className="badge-tag">AI Legal Analyzer • Bảng C</span>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <div className="privacy-badge">
          <ShieldAlert size={15} color="#10b981" />
          <span>Zero-Persistence • Tuân thủ NĐ 13/2023/NĐ-CP</span>
        </div>
        {hasResult && onReset && (
          <button className="btn-sample" onClick={onReset}>
            <FileText size={15} />
            <span>Phân tích hợp đồng mới</span>
          </button>
        )}
      </div>
    </header>
  );
};
