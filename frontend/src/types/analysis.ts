export type RiskLabelId =
  | 'UNFAIR_PENALTY'
  | 'UNILATERAL_MODIFICATION'
  | 'AMBIGUOUS_LIABILITY'
  | 'MISSING_JURISDICTION'
  | 'PERSONAL_DATA_VIOLATION'
  | 'EXCESSIVE_TERMINATION'
  | 'HIDDEN_FEE'
  | 'FORCE_MAJEURE_GAP';

export interface RiskLabelInfo {
  id: RiskLabelId;
  nameVi: string;
  legalBasis: string;
  baseSeverity: number;
}

export interface ClauseResult {
  id: string;
  clauseNumber: string;
  title: string;
  text: string;
  severity: number; // 0 - 100
  labels: RiskLabelId[];
  explanation: string;
  legalCitation: string;
  recommendation: string;
  pageNumber?: number;
}

export interface AnalysisResult {
  contractTitle: string;
  contractType: 'LABOR' | 'LEASE' | 'SALES' | 'SERVICE';
  overallScore: number; // 0 - 100
  statusGrade: 'AN_TOAN' | 'CANH_BAO' | 'RUI_RO_CAO';
  summary: {
    totalClauses: number;
    riskyClauses: number;
    criticalCount: number;
    highCount: number;
    mediumCount: number;
  };
  clauses: ClauseResult[];
  analyzedAt: string;
}

export type AnalysisStep = 'IDLE' | 'PARSING' | 'CLASSIFYING' | 'SCORING' | 'SEARCHING_LAW' | 'COMPLETED';
