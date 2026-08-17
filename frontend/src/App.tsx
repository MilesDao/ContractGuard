import React from 'react';
import { Header } from './components/Header/Header';
import { UploadZone } from './components/UploadZone/UploadZone';
import { AnalysisProgress } from './components/AnalysisProgress/AnalysisProgress';
import { DocumentViewer } from './components/DocumentViewer/DocumentViewer';
import { RiskPanel } from './components/RiskPanel/RiskPanel';
import { ExportReport } from './components/ExportReport/ExportReport';
import { useContractAnalysis } from './hooks/useContractAnalysis';

export const App: React.FC = () => {
  const {
    step,
    selectedFile,
    result,
    selectedClauseId,
    setSelectedClauseId,
    uploadAndAnalyze,
    loadSampleContract,
    resetAnalysis,
  } = useContractAnalysis();

  return (
    <div className="app-container">
      <Header onReset={resetAnalysis} hasResult={step === 'COMPLETED'} />

      <main className="main-content">
        {step === 'IDLE' && (
          <UploadZone
            onFileUpload={uploadAndAnalyze}
            onSelectSample={loadSampleContract}
          />
        )}

        {step !== 'IDLE' && step !== 'COMPLETED' && (
          <AnalysisProgress step={step} fileName={selectedFile?.name} />
        )}

        {step === 'COMPLETED' && result && (
          <div>
            <ExportReport result={result} />
            <div className="results-grid">
              <DocumentViewer
                contractTitle={result.contractTitle}
                clauses={result.clauses}
                selectedClauseId={selectedClauseId}
                onSelectClause={setSelectedClauseId}
              />
              <RiskPanel
                result={result}
                selectedClauseId={selectedClauseId}
                onSelectClause={setSelectedClauseId}
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
