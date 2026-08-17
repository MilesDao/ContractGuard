# 🛡️ HACKATHON_PLAN — ContractGuard

> **AI-Powered Vietnamese Contract Risk Analyzer**
> Sáng tạo AI 2026 — Bảng C | Option A (PhoBERT Self-Trained)
> Team: AI Student 1 (Backend/ML) · AI Student 2 (Frontend) · Law Student (Legal)
> Engineering baseline: ECC rules (common, python, fastapi, react, web-security)

---

## 1. Project Overview

ContractGuard lets any Vietnamese individual or SME upload a contract (PDF / DOCX) and receive, in under 8 seconds:

- Clause-level **risk labels** grounded in Vietnamese statute
- A **severity score** (0–100) per clause and an overall contract health grade
- **Highlighted danger zones** overlaid directly on the document viewer
- **Legally-grounded remediation suggestions** with exact article citations
- A downloadable **Risk Report PDF**

The system's unique edge: every output is validated against a legal taxonomy built by the law student, fulfilling the Bảng C judging criteria on *data compliance*, *AI mastery*, *ethics & responsibility*, and *practical deployability* simultaneously.

---

## 2. Tech Stack

### 2.1 Backend (AI Student 1)

| Layer | Technology | ECC Rule Basis |
|---|---|---|
| Runtime | Python 3.11 | `python-coding-style` |
| API Framework | **FastAPI** with `create_app()` factory | `python-fastapi` — thin routers, services layer |
| Async I/O | `async def` on all endpoints; `httpx` for async HTTP | `python-fastapi` — no blocking calls in async routes |
| Schema validation | **Pydantic v2** models; separate Request / Response schemas | `python-fastapi` — keep schemas separate |
| Document parsing | **PyMuPDF** (`fitz`) for PDF bbox extraction; `python-docx` | |
| Vietnamese NLP | **underthesea** `word_tokenize` (required for PhoBERT) | |
| ML framework | **PyTorch 2.x** + **HuggingFace Transformers** | |
| Core model | `vinai/phobert-base` fine-tuned (multi-label classifier) | |
| Recommendation | **FAISS** local vector index + `bkai-foundation-models/vietnamese-bi-encoder` | |
| Legal corpus | `undertheseanlp/UTS_VLC` (HuggingFace — public domain) | |
| Rate limiting | `slowapi` (per-IP on `/api/analyze`) | `common-security`, `python-fastapi` |
| CORS | Env-specific origins; no wildcard + credentials | `python-fastapi` — CORS env-specific |
| Code quality | `black`, `isort`, `ruff` | `python-coding-style` |
| Testing | `pytest` + `pytest-asyncio`; async test client | `python-fastapi` — prefer async test clients |

### 2.2 Frontend (AI Student 2)

| Layer | Technology | ECC Rule Basis |
|---|---|---|
| Framework | **React 18** + **Vite** | `react-coding-style` |
| Language | **TypeScript (.tsx / .ts)** | `react-coding-style` — `.tsx` for JSX files |
| PDF viewer + highlights | **react-pdf-highlighter-plus** | viewport-independent coordinate system |
| Styling | **Vanilla CSS** + CSS custom properties | workspace rules; `web-coding-style` |
| State | `useState` local → `useContext` for cross-component | `react-coding-style` — local first, lift only when shared |
| HTTP | **Axios** with upload progress | |
| PDF export | **jsPDF** + `html2canvas` (client-side only) | |
| Security | No `dangerouslySetInnerHTML`; all env secrets server-side only | `react-security` — CRITICAL XSS rule |
| CSP headers | Served by FastAPI: `default-src 'self'; frame-src 'none'` | `web-security` — nonce-based CSP |
| Security headers | HSTS, X-Frame-Options: DENY, X-Content-Type-Options: nosniff | `web-security` |

### 2.3 ML Model Architecture (Option A — Self-Trained)

```
vinai/phobert-base
    ↓
[CLS] token (768-dim)
    ↓
Dropout(p=0.3)
    ↓
Linear(768 → 256) + GELU
    ↓
Linear(256 → 8)           ← 8 risk label nodes
    ↓
Sigmoid()                 ← independent probabilities per label
```

- **Loss:** `BCEWithLogitsLoss` with per-class positive weights
- **Optimizer:** AdamW, lr=2e-5, warmup_ratio=0.1
- **Max length:** 256 tokens (covers 95%+ of contract clauses)
- **Threshold:** 0.5 per label (tunable post-training)
- **Preprocessing:** `underthesea.word_tokenize(text, format="text")` → underscore-joined segments

---

## 3. System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Browser                             │
│                                                                 │
│  ┌──────────────┐    ┌──────────────────┐    ┌───────────────┐  │
│  │  UploadZone  │───▶│ AnalysisProgress │───▶│ ResultsView   │  │
│  │  .tsx        │    │ .tsx             │    │ (Split Panel) │  │
│  └──────────────┘    └──────────────────┘    │               │  │
│                                              │ ┌───────────┐ │  │
│                                              │ │ PDFViewer │ │  │
│                                              │ │ +Highlights│ │  │
│                                              │ └───────────┘ │  │
│                                              │ ┌───────────┐ │  │
│                                              │ │ RiskPanel │ │  │
│                                              │ │ +RiskCards│ │  │
│                                              │ └───────────┘ │  │
│                                              └───────────────┘  │
└─────────────────────────┬───────────────────────────────────────┘
                          │ POST /api/analyze (multipart)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                               │
│                                                                 │
│  ┌───────────┐  ┌──────────────┐  ┌─────────────────────────┐  │
│  │  Router   │─▶│AnalysisService│─▶│       Pipeline          │  │
│  │ (thin)    │  │ (business)   │  │                         │  │
│  └───────────┘  └──────────────┘  │ 1. DocumentParser       │  │
│                                   │    PyMuPDF / python-docx│  │
│                                   │ 2. ClauseSegmenter      │  │
│                                   │    Rule-based + regex   │  │
│                                   │ 3. PhoBERTClassifier    │  │
│                                   │    Fine-tuned (local)   │  │
│                                   │ 4. SeverityScorer       │  │
│                                   │    Weighted formula     │  │
│                                   │ 5. Recommender (RAG)    │  │
│                                   │    FAISS + bi-encoder   │  │
│                                   └─────────────────────────┘  │
│                                                                 │
│  ⚠️  Privacy: file bytes live in memory only — NEVER written    │
│     to disk. Deleted from memory in finally block.             │
└─────────────────────────────────────────────────────────────────┘
```

### API Contract

```
POST /api/analyze
  Content-Type: multipart/form-data
  Body: { file: File }  (PDF or DOCX, max 10 MB)
  Response 200: AnalysisResult
  Response 400: { success: false, error: "Invalid file type / size" }
  Response 429: { success: false, error: "Rate limit exceeded" }

GET /api/health
  Response 200: { status: "ok", model_loaded: true }

GET /api/labels
  Response 200: { labels: [{ id, name_vi, legal_basis, severity_base }] }
```

### Immutable API Envelope (ECC `common-patterns` — API Response Format)

```python
# schemas/response.py
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)          # immutable — ECC common-coding-style
class ApiResponse:
    success: bool
    data: Any | None
    error: str | None
    meta: dict | None = None
```

---

## 4. Project Directory Structure

```
contractguard/
├── backend/
│   ├── main.py               # create_app() factory — ECC fastapi rule
│   ├── routers/
│   │   └── analyze.py        # thin router — delegates to service
│   ├── services/
│   │   └── analysis_service.py  # orchestrates pipeline
│   ├── pipeline/
│   │   ├── parser.py         # PyMuPDF + python-docx extraction
│   │   ├── segmenter.py      # clause boundary detection
│   │   ├── classifier.py     # PhoBERT inference wrapper
│   │   ├── scorer.py         # severity computation (pure functions)
│   │   └── recommender.py    # FAISS RAG lookup
│   ├── schemas/
│   │   ├── request.py        # UploadRequest schema
│   │   └── response.py       # AnalysisResult, ClauseResult, ApiResponse
│   ├── core/
│   │   ├── config.py         # Settings from env (no hardcoded secrets)
│   │   ├── privacy.py        # memory-safe file lifecycle
│   │   └── rate_limit.py     # slowapi setup
│   ├── tests/
│   │   ├── test_pipeline.py
│   │   ├── test_privacy.py   # assert no disk writes
│   │   └── test_api.py
│   └── requirements.txt
│
├── model/
│   ├── train.py              # PhoBERT fine-tuning entry point
│   ├── evaluate.py           # Macro F1, Hamming Loss, per-label P/R
│   ├── build_index.py        # FAISS index from UTS_VLC corpus
│   └── checkpoints/          # saved model (gitignored if >100MB)
│
├── data/
│   ├── annotated/
│   │   └── clauses_annotated.csv   # Law student ground truth
│   ├── legal_corpus/         # UTS_VLC raw texts (gitignored)
│   └── faiss_index/          # pre-built index (checked in as artifact)
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── UploadZone/
│   │   │   │   ├── UploadZone.tsx
│   │   │   │   ├── UploadZone.css
│   │   │   │   └── index.ts
│   │   │   ├── AnalysisProgress/
│   │   │   ├── PDFViewer/
│   │   │   ├── RiskPanel/
│   │   │   ├── RiskCard/
│   │   │   ├── SeverityGauge/
│   │   │   └── ExportReport/
│   │   ├── hooks/
│   │   │   └── useContractAnalysis.ts   # custom hook, camelCase
│   │   ├── types/
│   │   │   └── analysis.ts              # AnalysisResult, ClauseResult types
│   │   └── styles/
│   │       └── index.css
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
└── legal/
    ├── risk_taxonomy.md
    ├── annotation_guidelines.md
    ├── ethics_audit_report.md    ← KEY DIFFERENTIATOR
    └── disclaimer.md
```

---

## 5. Risk Taxonomy (8 Labels — Law Student Authored)

| ID | Label | Vietnamese Name | Legal Basis | Base Severity |
|---|---|---|---|---|
| L1 | `UNFAIR_PENALTY` | Điều khoản phạt bất hợp lý | BLDS 2015, Điều 418; Luật BVNTD Điều 16 | 85 |
| L2 | `UNILATERAL_MODIFICATION` | Sửa đổi đơn phương | BLDS 2015, Điều 421 | 90 |
| L3 | `AMBIGUOUS_LIABILITY` | Trách nhiệm mơ hồ | BLDS 2015, Điều 351–360 | 70 |
| L4 | `MISSING_JURISDICTION` | Thiếu điều khoản giải quyết tranh chấp | Luật Trọng tài TM Điều 5 | 65 |
| L5 | `PERSONAL_DATA_VIOLATION` | Vi phạm quyền riêng tư dữ liệu | NĐ 13/2023, Điều 9–11 | 95 |
| L6 | `EXCESSIVE_TERMINATION` | Điều khoản chấm dứt bất lợi | BLLĐ 2019, Điều 34–36 | 75 |
| L7 | `HIDDEN_FEE` | Phí ẩn / chi phí không minh bạch | Luật BVNTD Điều 10 | 80 |
| L8 | `FORCE_MAJEURE_GAP` | Thiếu / bất hợp lý bất khả kháng | BLDS 2015, Điều 156 | 55 |

---

## 6. Core Code Patterns (ECC-Compliant)

### 6.1 FastAPI Application Factory

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from backend.core.config import Settings
from backend.routers import analyze

def create_app(settings: Settings | None = None) -> FastAPI:
    """ECC rule: put app construction in create_app()."""
    cfg = settings or Settings()
    app = FastAPI(title="ContractGuard API", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cfg.CORS_ORIGINS,   # env-specific — ECC fastapi rule
        allow_methods=["POST", "GET"],
        allow_headers=["Content-Type"],
        allow_credentials=False,           # no wildcard + credentials
    )
    app.include_router(analyze.router, prefix="/api")
    return app
```

### 6.2 Privacy-Safe File Handling (ECC `common-security`)

```python
# backend/core/privacy.py
from contextlib import contextmanager

@contextmanager
def ephemeral_bytes(file_bytes: bytes):
    """
    Guarantees file bytes are zeroed and deleted after processing.
    Never written to disk — ECC: validate at system boundaries,
    never trust external data.
    """
    try:
        yield file_bytes
    finally:
        # Overwrite in-place before GC
        file_bytes = b"\x00" * len(file_bytes)
        del file_bytes

# backend/routers/analyze.py
@router.post("/analyze", response_model=ApiResponse)
async def analyze_contract(
    file: UploadFile = File(...),
    _: None = Depends(rate_limit_dep),
):
    # ECC: validate all user input at system boundaries
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(400, "Only PDF and DOCX files are accepted")
    if file.size and file.size > MAX_FILE_BYTES:
        raise HTTPException(400, "File exceeds 10 MB limit")

    content = await file.read()

    with ephemeral_bytes(content) as raw:
        result = await analysis_service.run(raw, file.filename)

    # ECC: consistent API envelope
    return ApiResponse(success=True, data=result, error=None)
```

### 6.3 Pure-Function Severity Scorer (ECC Immutability)

```python
# backend/pipeline/scorer.py
from dataclasses import dataclass
from typing import Mapping

BASE_SEVERITY: Mapping[str, int] = {
    "PERSONAL_DATA_VIOLATION":   95,
    "UNILATERAL_MODIFICATION":   90,
    "UNFAIR_PENALTY":            85,
    "HIDDEN_FEE":                80,
    "EXCESSIVE_TERMINATION":     75,
    "AMBIGUOUS_LIABILITY":       70,
    "MISSING_JURISDICTION":      65,
    "FORCE_MAJEURE_GAP":         55,
}

THRESHOLD: float = 0.5

@dataclass(frozen=True)          # ECC: immutable — ALWAYS create new objects
class ClauseScore:
    clause_id: str
    severity: int
    active_labels: tuple[str, ...]

def score_clause(clause_id: str, probs: Mapping[str, float]) -> ClauseScore:
    """Pure function — ECC common-coding-style: no mutation."""
    active = tuple(
        label for label, prob in probs.items()
        if prob >= THRESHOLD
    )
    severity = max(
        (int(BASE_SEVERITY[lbl] * probs[lbl]) for lbl in active),
        default=0,
    )
    return ClauseScore(clause_id=clause_id, severity=severity, active_labels=active)
```

### 6.4 React Component Shape (ECC `react-coding-style`)

```tsx
// frontend/src/components/RiskCard/RiskCard.tsx
import type { ClauseResult } from "../../types/analysis";

type Props = {
  clause: ClauseResult;
  onFocus: (clauseId: string) => void;
};

export function RiskCard({ clause, onFocus }: Props) {
  // ECC: group hooks at top, before any conditional logic
  const isHighRisk = clause.severity >= 70;

  const handleFocus = () => onFocus(clause.id);   // ECC: handleVerb naming

  return (
    <article
      className={`risk-card ${isHighRisk ? "risk-card--high" : "risk-card--medium"}`}
      onClick={handleFocus}
    >
      <header className="risk-card__header">
        <span className="risk-card__id">{clause.id}</span>
        <SeverityBadge score={clause.severity} />
      </header>
      <p className="risk-card__preview">
        {clause.text.slice(0, 120)}…
      </p>
      <ul className="risk-card__labels">
        {clause.labels.map((label) => (
          <RiskLabel key={label.id} label={label} />
        ))}
      </ul>
      <section className="risk-card__recommendation">
        <h3>💡 Khuyến nghị</h3>
        <p>{clause.recommendation}</p>
        <cite>{clause.legalCitation}</cite>
      </section>
    </article>
  );
}
```

---

## 7. Regulatory Compliance Goals
### (Law Student Drafts — referenced as source-of-truth for implementation)

### 7.1 Scope of System Output
- ContractGuard provides **risk information** (thông tin cảnh báo), NOT **legal advice** (tư vấn pháp lý)
- Disclaimer must appear on every analysis result page and in the exported report
- Legal basis: Luật Luật sư 2006, sửa đổi 2012 — Article 22 defines the unauthorized practice boundary

### 7.2 Personal Data Handling (Nghị định 13/2023/NĐ-CP)

| Requirement (NĐ 13) | Implementation |
|---|---|
| Điều 9 — Mục đích xử lý rõ ràng | Privacy notice on upload screen: "File xử lý để phân tích rủi ro và bị xóa ngay" |
| Điều 10 — Giới hạn lưu trữ | Zero persistence: `ephemeral_bytes()` context manager; no DB, no disk writes |
| Điều 11 — Bảo mật dữ liệu | HTTPS required; server memory only; no logging of file content |
| Điều 21 — Quyền xóa dữ liệu | Moot — nothing is stored; document this explicitly in ethics report |

### 7.3 Data Provenance (Bảng C Criterion: Nguồn gốc dữ liệu rõ ràng)

| Dataset | Source | License | Usage |
|---|---|---|---|
| Training contracts | Official templates (Bộ LĐ, VCCI, Bộ XD) | Public domain | Training + annotation |
| Legal corpus | UTS_VLC — vbpl.vn official | Public domain (Chính phủ Việt Nam) | RAG index |
| Annotations | Hand-labeled by Law Student | Original work by team | Ground truth |
| PhoBERT weights | VinAI Research (Apache 2.0) | Apache 2.0 | Fine-tuning |

### 7.4 AI Ethics Audit Report Sections (Law Student Authors)

```
1. System boundary & liability disclaimer
2. Data provenance table (complete)
3. Bias testing results (F1 per contract type)
4. NĐ 13/2023 compliance matrix (article-by-article)
5. AI limitations statement (dialects, handwritten, non-standard)
6. Human override procedure (what if AI is wrong?)
7. Post-hackathon improvement roadmap
8. Acknowledgement of Vietnam AI Ethics Framework (Dec 2025)
```

### 7.5 Intellectual Property

- No copyrighted contract templates used without permission
- All vbpl.vn statutory text is public domain by Vietnamese law
- PhoBERT used under Apache 2.0 — commercial use permitted
- Team retains copyright over: annotations, fine-tuned weights, codebase

---

## 8. Milestone Breakdown — Hour 1 to Hour 24

> Assumes a **concentrated 24-hour sprint** (hackathon day). Pre-work (data annotation) done in the days before.

### PRE-SPRINT (Days before the 24-hour window)
| Owner | Task | Done When |
|---|---|---|
| Law | Collect 60–80 real contracts (PDF/DOCX) | Folder with 80 contracts |
| Law | Complete annotation of 200+ clauses in CSV | `clauses_annotated.csv` ≥200 rows |
| Law | Draft risk taxonomy + annotation guidelines | `legal/risk_taxonomy.md` written |
| AI 1 | Set up Python env, install torch + transformers | `pip install` succeeds |
| AI 1 | Run PhoBERT fine-tuning (takes 2–6 hours on GPU) | `model/checkpoints/best.pt` saved |
| AI 2 | Scaffold Vite + React + TypeScript project | `npm run dev` runs |

---

### HOUR 1–3 | Foundation & Integration Kickoff

| Owner | Task | Deliverable |
|---|---|---|
| AI 1 | `create_app()` factory, CORS, rate limiting, health endpoint | `GET /api/health` → 200 |
| AI 1 | Load trained PhoBERT checkpoint into `classifier.py` | Inference returns probs in <500ms |
| AI 1 | `DocumentParser.parse_pdf()` with bbox extraction | Returns clause list with page+bbox |
| AI 2 | `UploadZone.tsx` — drag & drop, file type/size validation | File selected → `onUpload(file)` fires |
| AI 2 | Axios hook `useContractAnalysis.ts` — POST with progress | State: idle → uploading → analyzing |
| Law | Finalize disclaimer text + privacy notice copy | `legal/disclaimer.md` complete |

### HOUR 4–6 | Core Pipeline Connected

| Owner | Task | Deliverable |
|---|---|---|
| AI 1 | `POST /api/analyze` endpoint — end-to-end with real model | Returns `AnalysisResult` JSON |
| AI 1 | `SeverityScorer` pure functions — per-clause + contract grade | Score + risk level in response |
| AI 1 | FAISS index loaded; `Recommender.lookup()` returns suggestion | Recommendation text per label |
| AI 2 | `AnalysisProgress.tsx` — animated step indicators | 3-stage animation: Parse → Analyze → Score |
| AI 2 | Wire upload to `POST /api/analyze`; parse response | Full JSON received and logged |
| Law | Cross-check 20 classifier outputs against legal expectation | Written feedback list to AI 1 |

### HOUR 7–10 | UI Results View

| Owner | Task | Deliverable |
|---|---|---|
| AI 2 | `PDFViewer.tsx` — render PDF with `react-pdf-highlighter-plus` | PDF renders in browser |
| AI 2 | Map API `bbox` coordinates → highlight positions on PDF | RED/ORANGE/YELLOW overlays visible |
| AI 2 | `RiskPanel.tsx` + `RiskCard.tsx` — collapsible cards with labels | Panel lists all risky clauses |
| AI 2 | `SeverityGauge.tsx` — SVG arc gauge for contract health score | Gauge animates 0→score on mount |
| AI 1 | Error handling: 400 (bad file), 429 (rate limit) → clean JSON | All errors use `ApiResponse` envelope |
| Law | Write Section 1–4 of AI Ethics Audit Report | Ethics report 50% done |

### HOUR 11–14 | Polish & Export

| Owner | Task | Deliverable |
|---|---|---|
| AI 2 | `ExportReport.tsx` — jsPDF renders report with clause table | "Tải báo cáo PDF" button works |
| AI 2 | Responsive CSS — mobile & tablet breakpoints | Works at 375px, 768px, 1280px |
| AI 2 | Click risk card → scroll + flash highlight in PDF viewer | Bidirectional navigation works |
| AI 2 | Empty state, error state, loading skeleton UIs | No blank screens |
| AI 1 | Privacy test: assert no temp files remain after `/analyze` | `test_privacy.py` passes |
| Law | Write Section 5–8 of AI Ethics Audit Report | Ethics report 100% done |

### HOUR 15–18 | Testing & Model Evaluation

| Owner | Task | Deliverable |
|---|---|---|
| AI 1 | Run `evaluate.py` on 20% held-out set | Macro F1 report printed |
| AI 1 | `pytest tests/` — all 3 test files pass | ✅ green CI output |
| AI 2 | `npm run build` — no TypeScript errors | Production bundle builds |
| All | End-to-end test: upload 5 real contracts (different types) | All return results; no crashes |
| Law | Validate AI outputs for 5 test contracts vs. legal expectation | Pass/fail notes documented |
| All | Fix critical bugs found in E2E testing | Bug tracker cleared |

### HOUR 19–21 | Demo Video Recording (5 min)

```
Script:
00:00–00:30  Problem statement: "90% SME ký hợp đồng không có luật sư"
00:30–01:00  Upload a real hợp đồng lao động → watch analysis in real time
01:00–02:30  Walk through results: PDF with highlights, risk cards, severity gauge
02:30–03:30  Click clause → explain legal basis + recommendation
03:30–04:00  Export risk report PDF
04:00–04:30  Architecture overview (diagram)
04:30–05:00  Team intro + unique advantage (Law student authored the AI's taxonomy)
```

### HOUR 22–24 | Submission Document (PDF, ≤20 trang)

| Section | Owner | Pages |
|---|---|---|
| Bìa + Mục lục | AI 2 | 2 |
| Xác định bài toán + tính cấp thiết | Law | 2 |
| Phương pháp & kiến trúc hệ thống | AI 1 | 3 |
| Dữ liệu: nguồn gốc, quy trình, tính hợp lệ | Law + AI 1 | 2 |
| Mô hình AI: PhoBERT, huấn luyện, đánh giá | AI 1 | 3 |
| Đạo đức AI & tuân thủ pháp luật | Law | 3 |
| Kết quả thử nghiệm & phân tích lỗi | AI 1 | 2 |
| Khả năng triển khai & mở rộng | All | 1 |
| Kết luận | All | 1 |
| Tài liệu tham khảo | All | 1 |

---

## 9. Validation Matrix — Metrics to Hit Before Judging

### 9.1 ML Model Metrics

| Metric | Target | Measurement Method |
|---|---|---|
| Macro F1 (overall) | **≥ 0.65** | `evaluate.py` on 20% held-out split |
| Micro F1 | ≥ 0.70 | `evaluate.py` |
| Hamming Loss | **≤ 0.15** | `evaluate.py` |
| Per-label Precision (avg) | ≥ 0.60 | `evaluate.py` per-label table |
| Per-label Recall (avg) | ≥ 0.60 | `evaluate.py` per-label table |
| `PERSONAL_DATA_VIOLATION` F1 | **≥ 0.70** | Priority label — top judging concern |
| Training clauses | **≥ 200** | Count rows in `clauses_annotated.csv` |

### 9.2 System Performance

| Metric | Target | Measurement Method |
|---|---|---|
| End-to-end analysis latency (5-page PDF) | **< 8 seconds** | Browser Network tab timer |
| API `/analyze` p95 latency | < 10s | `pytest` benchmark |
| Frontend build — no TypeScript errors | ✅ 0 errors | `npm run build` exit code 0 |
| All backend tests pass | ✅ `pytest` green | `pytest tests/ -v` |
| Privacy test: no disk writes | ✅ PASS | `test_privacy.py` |
| Rate limit: >10 req/min/IP → 429 | ✅ PASS | `test_api.py` |

### 9.3 Legal Compliance Checklist

| Item | Target | Owner |
|---|---|---|
| All 8 risk labels have legal article citation | ✅ 8/8 | Law |
| Privacy notice visible on upload screen | ✅ visible | AI 2 |
| Disclaimer on results page + exported report | ✅ present | AI 2 + Law |
| `ephemeral_bytes()` in `test_privacy.py` passes | ✅ PASS | AI 1 |
| Data provenance table complete | ✅ complete | Law |
| AI Ethics Audit Report written | ✅ PDF submitted | Law |
| No contract file persisted to disk or DB | ✅ verified | AI 1 |

### 9.4 UX / Demo Quality

| Item | Target | Owner |
|---|---|---|
| Contract types tested | ≥ 3 types | All |
| Responsive at 375px / 768px / 1280px | ✅ no overflow | AI 2 |
| PDF highlights correctly mapped to clauses | ✅ verified | AI 2 |
| Export PDF report readable on mobile | ✅ verified | AI 2 |
| Demo video smooth, no crashes | ≤ 5 min video | All |
| Submission PDF ≤ 20 pages | ✅ checked | All |

### 9.5 Bảng C Judge Criteria Checklist

| Bảng C Tiêu chí | Our Evidence | Score Target |
|---|---|---|
| Tính cấp thiết & tác động | Market data (90% SME no legal review) in PDF | HIGH |
| Tính khoa học & logic | Architecture diagram + PhoBERT training pipeline | HIGH |
| Chất lượng dữ liệu & tính hợp lệ | Provenance table + annotation guidelines | HIGH |
| **Làm chủ mô hình & kiến trúc** | **Self-trained PhoBERT — not just API calls** | **CRITICAL** |
| Kết quả thử nghiệm & kiểm chứng | F1 scores, confusion matrix, 5-contract E2E test | HIGH |
| Phân tích lỗi & rủi ro | Model limitations section in ethics report | HIGH |
| **Đạo đức AI & trách nhiệm** | **AI Ethics Audit Report by Law student** | **CRITICAL** |
| Tính sáng tạo & khả thi | Cross-discipline team + deploy-ready API design | HIGH |
| Khả năng triển khai & mở rộng | API-first; add contract types without full retraining | HIGH |

---

## 10. ECC Engineering Rules Applied

> Summary of ECC rules baked into this plan. Every code decision traces back to a rule.

| ECC Rule | Applied Where |
|---|---|
| `create_app()` factory pattern | `backend/main.py` |
| Thin routers → service layer | `backend/routers/` delegates to `services/` |
| Separate Request / Response schemas | `backend/schemas/request.py` + `response.py` |
| `async def` on all endpoints; no blocking in async routes | All FastAPI routes |
| CORS origins env-specific; no wildcard + credentials | `backend/core/config.py` → env var |
| Rate-limit write-heavy endpoints | `slowapi` on `/api/analyze` |
| Never log credentials / file content | `backend/core/privacy.py` |
| **ALWAYS create new objects, NEVER mutate** | `ClauseScore(frozen=True)`, `ApiResponse(frozen=True)` |
| Functions < 50 lines; files < 800 lines | All modules organized by feature |
| No deep nesting (>4 levels) | Early returns + context manager pattern |
| Validate all user input at system boundaries | File type + size check before reading bytes |
| Schema-based validation | Pydantic v2 on all request/response models |
| No hardcoded secrets | All config via `Settings` from env vars |
| `.tsx` for JSX files | All React component files |
| `PascalCase` components, `handleVerb` event handlers | `RiskCard.tsx`, `handleFocus` |
| `useCamelCase` for hooks | `useContractAnalysis.ts` |
| No `dangerouslySetInnerHTML` without DOMPurify | Zero usage in codebase |
| No secrets in `VITE_*` env vars | Only `VITE_API_BASE_URL` (non-secret) exposed to client |
| CSP headers: `frame-src 'none'`, `default-src 'self'` | FastAPI middleware |
| Security headers (HSTS, X-Frame-Options, etc.) | FastAPI middleware |
| `target="_blank"` → `rel="noopener noreferrer"` | All external links |
| Consistent API response envelope | `ApiResponse(success, data, error, meta)` |
| Repository pattern for data access | `FAISS` access abstracted behind `Recommender` class |

---

*Generated: 2026-08-12 | ContractGuard v1.0 | Sáng tạo AI 2026 — Bảng C*
