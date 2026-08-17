# 🛡️ ContractGuard — Team Overview

> **AI-Powered Vietnamese Contract Risk Analyzer**
> Cuộc thi Sáng tạo AI 2026 — Bảng C
> Last updated: 2026-08-12

---

## 👥 Team & Roles At a Glance

| Member | Role | Core Responsibility |
|---|---|---|
| **AI Student 1** | Backend & ML Engineer | Build the AI brain — model training, API, data pipeline |
| **AI Student 2** | Frontend Engineer | Build the UI — PDF viewer, risk dashboard, export |
| **Law Student** | Legal Architect | Define risk rules, annotate data, write ethics audit |

> 💡 **What makes us different from every other team:** We have a Law student who validates the AI's outputs using real Vietnamese law. No other AI-only team can do this.

---

## 🎯 What Are We Building?

**ContractGuard** is a web app that lets anyone upload a Vietnamese contract (PDF/DOCX) and get an instant AI-powered risk report — highlighting dangerous clauses, explaining *why* they're risky (with exact legal article citations), and suggesting safer alternatives.

### The User Journey

```
1. User uploads contract (PDF or DOCX)
         ↓
2. AI reads and segments it into clauses
         ↓
3. AI flags risky clauses with labels + severity score (0–100)
         ↓
4. Results shown on split screen:
   LEFT: PDF with color-coded highlights  |  RIGHT: Risk cards with explanations
         ↓
5. User downloads a Risk Report PDF
```

### Demo Flow (5-min video)
```
Upload hợp đồng lao động → analysis runs in < 8 seconds
→ PDF lights up: RED clauses (critical), ORANGE (high), YELLOW (medium)
→ Click a clause → see: risk label + legal basis + recommended fix
→ Export full report as PDF
```

---

## 🏗️ System Architecture (Simple View)

```
┌─────────────────────────────────────────────────────────┐
│                  USER'S BROWSER                         │
│                                                         │
│   [Upload Zone] → [Progress] → [PDF Viewer | Risk Panel]│
│        ↑ AI Student 2 builds this entire layer          │
└──────────────────────┬──────────────────────────────────┘
                       │  sends contract file via API
                       ↓
┌─────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI)                       │
│                                                         │
│  Step 1: Parse contract → extract clauses + positions   │
│  Step 2: Classify each clause → 8 risk labels           │
│  Step 3: Score severity (0–100) per clause              │
│  Step 4: Fetch legal article + recommendation (RAG)     │
│                                                         │
│  ⚠️  Contract file is NEVER saved to disk               │
│  ↑ AI Student 1 builds this entire layer                │
└──────────────────────┬──────────────────────────────────┘
                       │ uses
         ┌─────────────┴─────────────┐
         ↓                           ↓
  [PhoBERT Model]            [FAISS Vector DB]
  Fine-tuned on              Vietnamese legal
  Vietnamese contracts       corpus (UTS_VLC)
  → outputs risk labels      → outputs legal articles
                             + recommendations
```

---

## ⚖️ The 8 Risk Labels (Law Student Designed These)

Every label is grounded in **real Vietnamese law**:

| # | Label | Vietnamese Name | Legal Basis | Severity |
|---|---|---|---|---|
| 1 | `UNFAIR_PENALTY` | Điều khoản phạt bất hợp lý | BLDS 2015, Điều 418 | 85/100 |
| 2 | `UNILATERAL_MODIFICATION` | Sửa đổi đơn phương | BLDS 2015, Điều 421 | 90/100 |
| 3 | `AMBIGUOUS_LIABILITY` | Trách nhiệm mơ hồ | BLDS 2015, Điều 351–360 | 70/100 |
| 4 | `MISSING_JURISDICTION` | Thiếu điều khoản giải quyết tranh chấp | Luật TTTM, Điều 5 | 65/100 |
| 5 | `PERSONAL_DATA_VIOLATION` | Vi phạm quyền riêng tư dữ liệu | NĐ 13/2023, Điều 9–11 | **95/100** |
| 6 | `EXCESSIVE_TERMINATION` | Điều khoản chấm dứt bất lợi | BLLĐ 2019, Điều 34–36 | 75/100 |
| 7 | `HIDDEN_FEE` | Phí ẩn / không minh bạch | Luật BVNTD, Điều 10 | 80/100 |
| 8 | `FORCE_MAJEURE_GAP` | Thiếu điều khoản bất khả kháng | BLDS 2015, Điều 156 | 55/100 |

---

## 🤖 AI Stack (What We Actually Build)

### Model Choice: PhoBERT + Gemini Flash (Hybrid)

```
Every clause
    │
    ▼
[PhoBERT — self-trained] ← We built & trained this ourselves
    → Outputs: which of 8 labels apply + probability scores
    → Fast: < 100ms per clause
    → Runs locally (no API cost)
    │
    │ If severity ≥ 70 (dangerous clause)
    ▼
[Gemini Flash API] ← Generates human-readable explanation
    → Pulls exact legal article from FAISS database
    → Writes: "Why is this dangerous?" + "How to fix it?"
    → Free tier: 1,500 requests/day
```

**Why PhoBERT?** Because we *built it ourselves* — the judges specifically evaluate "mức độ làm chủ mô hình". Using only ChatGPT API would lose us points.

**Why Gemini for explanations?** Because PhoBERT can't write sentences. We use it only for the *text explanations*, not the classification.

---

## 📦 Data: Where It Comes From

### Training Data (for PhoBERT)

We collect real Vietnamese contracts and label them — but NOT manually one by one. We use a **3-layer auto-labeling pipeline**:

```
300 contract clauses
    │
    ├─ Layer 1: Keyword rules (instant, free)
    │   "đơn phương" → UNILATERAL_MODIFICATION ✅
    │   Covers ~60% of clauses automatically
    │
    ├─ Layer 2: Gemini auto-labels uncertain cases (~10 min)
    │   Covers another ~25% automatically
    │
    └─ Layer 3: Law student reviews only uncertain cases
        ~45 clauses × 3 min = ~2.5 hours total
        (instead of 50 hours if done fully manually)
```

### Where to Download Contracts
- **thuvienphapluat.vn** → search "mẫu hợp đồng"
- **fdvn.vn** → 50 standard templates
- **mauhopdong.vn** → 200+ templates by sector
- **molisa.gov.vn** → Official labor contract template

**Target:** 80 contracts → ~300 clauses → 250+ labeled training samples

### Legal Corpus (for RAG recommendations)
- `undertheseanlp/UTS_VLC` on HuggingFace — all Vietnamese laws, public domain, clean Markdown

---

## 🛠️ Full Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 18 + Vite + TypeScript |
| **PDF Viewer** | react-pdf-highlighter-plus |
| **Styling** | Vanilla CSS + CSS custom properties |
| **Backend** | FastAPI (Python 3.11) |
| **Document Parsing** | PyMuPDF (digital PDFs) |
| **Vietnamese NLP** | underthesea (word tokenizer) |
| **ML Model** | PhoBERT (vinai/phobert-base) fine-tuned |
| **ML Framework** | PyTorch + HuggingFace Transformers |
| **Recommendation** | FAISS + Gemini Flash API |
| **Legal Corpus** | UTS_VLC (HuggingFace) |
| **Auto-labeling** | Keyword rules + Gemini Flash |
| **Annotation Review** | Google Sheets (for law student) |
| **PDF Export** | jsPDF + html2canvas (client-side) |

---

## 📁 Project Structure

```
contractguard/
│
├── 📂 backend/                ← AI Student 1
│   ├── main.py                # FastAPI app entry point
│   ├── routers/               # API endpoints (thin)
│   ├── services/              # Business logic
│   ├── pipeline/              # parse → segment → classify → score → recommend
│   ├── schemas/               # Request/Response data models
│   └── core/                  # Config, privacy, rate limiting
│
├── 📂 model/                  ← AI Student 1
│   ├── train.py               # PhoBERT fine-tuning script
│   ├── evaluate.py            # F1 scores, Hamming Loss
│   ├── build_index.py         # Build FAISS index from legal corpus
│   └── checkpoints/           # Saved model weights
│
├── 📂 data/                   ← All 3 members
│   ├── raw_contracts/         # Downloaded contracts (gitignored)
│   ├── annotated/
│   │   └── clauses_annotated.csv   # Ground truth — Law student's work
│   ├── legal_corpus/          # UTS_VLC texts (gitignored)
│   └── faiss_index/           # Pre-built vector index
│
├── 📂 scripts/                ← AI Student 1
│   ├── extract_clauses.py     # PDF → clause list
│   ├── label_heuristics.py    # Layer 1: keyword auto-labeling
│   ├── label_with_llm.py      # Layer 2: Gemini auto-labeling
│   └── prepare_human_review.py # Layer 3: filter for law student
│
├── 📂 frontend/               ← AI Student 2
│   └── src/
│       ├── components/
│       │   ├── UploadZone/    # Drag & drop file upload
│       │   ├── PDFViewer/     # PDF with color highlights
│       │   ├── RiskPanel/     # List of risk cards
│       │   ├── RiskCard/      # Single clause risk details
│       │   ├── SeverityGauge/ # Contract health score (0–100)
│       │   └── ExportReport/  # Download PDF report
│       └── hooks/
│           └── useContractAnalysis.ts
│
└── 📂 legal/                  ← Law Student
    ├── risk_taxonomy.md       # 8 labels + legal basis (your core work)
    ├── annotation_guidelines.md # How to label clauses consistently
    ├── ethics_audit_report.md # AI Ethics Audit (KEY differentiator)
    └── disclaimer.md          # Legal disclaimer for users
```

---

## 📋 What Each Person Does — Week by Week

### Law Student Tasks

| Task | When | Output File |
|---|---|---|
| Write risk taxonomy (8 labels + legal articles) | Day 1 | `legal/risk_taxonomy.md` |
| Write annotation guidelines | Day 1–2 | `legal/annotation_guidelines.md` |
| Download 80+ contracts | Day 1–3 | `data/raw_contracts/` |
| Review ~45 auto-labeled clauses (Layer 3) | Day 3–5 | `data/annotated/clauses_annotated.csv` |
| Write legal disclaimer text | Day 4 | `legal/disclaimer.md` |
| Validate AI outputs on 5 test contracts | Day 7–8 | Written notes → AI Student 1 |
| Write AI Ethics Audit Report | Day 6–9 | `legal/ethics_audit_report.md` |
| Write submission PDF (legal sections) | Day 9–10 | Submission document |

**Your most important deliverable:** The **AI Ethics Audit Report** — no other team has a lawyer writing this. It directly answers the judging criterion *"đạo đức AI và trách nhiệm của đội thi"*.

---

### AI Student 1 Tasks

| Task | When | Output |
|---|---|---|
| Set up Python env + install dependencies | Day 1 | Working `pip install` |
| Write clause extraction scripts | Day 1–2 | `scripts/extract_clauses.py` |
| Run auto-labeling pipeline (Layers 1+2) | Day 2–3 | `data/clauses_auto_labeled.csv` |
| Fine-tune PhoBERT on annotated data | Day 3–6 | `model/checkpoints/best.pt` |
| Build FAISS index from UTS_VLC | Day 4 | `data/faiss_index/` |
| Build FastAPI backend + full pipeline | Day 5–7 | Running API at localhost:8000 |
| Write evaluation report (F1, metrics) | Day 8 | Metrics table for submission PDF |
| Privacy test (assert no disk writes) | Day 8 | `tests/test_privacy.py` passing |

---

### AI Student 2 Tasks

| Task | When | Output |
|---|---|---|
| Scaffold Vite + React + TypeScript project | Day 1 | `npm run dev` works |
| Build upload zone + progress animation | Day 2–3 | Upload UI |
| Build PDF viewer with color highlights | Day 3–5 | PDF renders with overlays |
| Build risk panel + expandable risk cards | Day 4–6 | Risk cards showing labels |
| Build severity gauge (0–100 arc chart) | Day 5 | Animated health score |
| Connect all UI to backend API | Day 6–7 | Full end-to-end working |
| Build PDF report export button | Day 8 | Download button works |
| Polish: mobile responsive, error states | Day 9 | Works on all screen sizes |

---

## ✅ What We Need to Achieve Before Submission

### Must-Hit Metrics

| What | Target |
|---|---|
| Model Macro F1 | **≥ 0.65** |
| Analysis time (5-page contract) | **< 8 seconds** |
| Annotated training clauses | **≥ 200** |
| Risk labels with legal citation | **8 / 8** |
| Privacy: no file saved to disk | **✅ Pass** |
| AI Ethics Audit Report | **Written & submitted** |
| Demo video | **≤ 5 minutes, no crashes** |
| Submission PDF | **≤ 20 pages** |

---

## 🔒 Privacy & Legal Compliance (Non-Negotiable)

> These are both **ethical requirements** AND **judging criteria**.

1. **Zero file persistence** — contracts are processed in memory only, deleted immediately after analysis. Never written to any file or database.
2. **User notice** — "File của bạn được xử lý trong bộ nhớ tạm và không được lưu trữ" shown on upload screen.
3. **Disclaimer on every result** — "ContractGuard cung cấp thông tin cảnh báo, KHÔNG thay thế tư vấn pháp lý."
4. **Data provenance** — every dataset used must be documented with source + license in submission PDF.
5. **Nghị định 13/2023** — our privacy approach complies article-by-article (law student documents this).

---

## 🗂️ Key Reference Documents in This Project

| Document | Location | Who Reads It |
|---|---|---|
| **This overview** | `TEAM_OVERVIEW.md` | Everyone |
| Full implementation plan | `HACKATHON_PLAN.md` | AI students (technical detail) |
| Data & model research | *(artifact)* | AI Student 1 |
| Auto-labeling pipeline | *(artifact)* | AI Student 1 |
| Risk taxonomy | `legal/risk_taxonomy.md` | Law student (to write), AI Student 1 |
| Ethics audit report | `legal/ethics_audit_report.md` | Law student (to write) |

---

## 💬 FAQ for Team Members

**Q: What contract types do we support for the demo?**
A: Hợp đồng lao động, thuê nhà, mua bán hàng hóa, dịch vụ — focus on these 4 types.

**Q: Do we need a GPU?**
A: Yes for training PhoBERT (Google Colab free tier works — T4 GPU). For the demo/deployment, it runs on CPU (slower but fine for judging).

**Q: What if our F1 score is low?**
A: A Macro F1 of 0.55–0.60 is still publishable for a hackathon. Be honest about limitations in the ethics report — judges respect transparency.

**Q: Does the law student need to write code?**
A: No. The law student works in Google Sheets (for annotation review) and Google Docs / Markdown (for legal documents).

**Q: What's the most important thing to demo?**
A: Upload a real contract → clauses light up on the PDF → click one → see the legal article citation + recommendation. If that works smoothly, we win.

**Q: How do we handle scanned (image-based) PDFs?**
A: MVP: show a warning banner — "PDF dạng scan chưa được hỗ trợ đầy đủ. Vui lòng dùng PDF dạng văn bản." This is honest and acceptable.

---

*ContractGuard — Built by a team that believes law and AI are better together.*
