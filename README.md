# 🛡️ ContractGuard — AI-Powered Vietnamese Contract Risk Analyzer

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PyTorch 2.x](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React 18](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org)
[![Vite](https://img.shields.io/badge/Vite-5.0+-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.style=for-the-badge)](LICENSE)

> **Cuộc thi Sáng tạo AI 2026 — Bảng C**
> **ContractGuard** là giải pháp trí tuệ nhân tạo chuyên sâu giúp cá nhân và doanh nghiệp nhỏ (SME) phân tích rủi ro pháp lý trong hợp đồng Việt Nam (PDF/DOCX) trong **dưới 8 giây** — tự động phát hiện các điều khoản bất lợi, trích dẫn chính xác Điều luật Việt Nam (BLDS 2015, BLLĐ 2019, NĐ 13/2023), tính toán chỉ số rủi ro (0–100) và đề xuất phương án sửa đổi an toàn.

---

## 📌 Table of Contents

- [✨ Key Features](#-key-features)
- [🏗️ System Architecture](#️-system-architecture)
- [👥 Team Structure & Roles](#-team-structure--roles)
- [⚖️ Risk Taxonomy (8 Categories)](#️-risk-taxonomy-8-categories)
- [🚀 3-Layer Data Auto-Labeling Pipeline](#-3-layer-data-auto-labeling-pipeline)
- [⚡ Model Fine-Tuning & Speed Optimizations](#-model-fine-tuning--speed-optimizations)
- [💻 Getting Started & Installation](#-getting-started--installation)
- [📊 Evaluation Metrics & Benchmarks](#-evaluation-metrics--benchmarks)
- [🔒 Privacy & Legal Compliance](#-privacy--legal-compliance)
- [📁 Project Structure](#-project-structure)

---

## ✨ Key Features

- ⚡ **Siêu Tốc**: Phân tích toàn bộ hợp đồng 5-10 trang trong **dưới 8 giây**.
- 🎯 **Làm Chủ Mô Hình**: Fine-tune trực tiếp **PhoBERT** (`vinai/phobert-base`) kết hợp FAISS Vector DB trích dẫn căn cứ pháp lý thay vì phụ thuộc hoàn toàn vào API đóng.
- 🎨 **Giao Diện Trực Quan (Split-Screen UI)**:
  - **Bên trái**: Trình xem văn bản hợp đồng tương tác với các vùng highlight màu sắc (Đỏ: Rủi ro cao, Cam: Cảnh báo).
  - **Bên phải**: Thước đo sức khỏe hợp đồng (Severity Gauge 0–100) và danh sách thẻ rủi ro chi tiết.
- ⚖️ **Căn Cứ Pháp Lý Chuẩn Xác**: Trích dẫn chính xác Điều luật (Bộ luật Dân sự 2015, Bộ luật Lao động 2019, Nghị định 13/2023/NĐ-CP bảo vệ dữ liệu cá nhân).
- 💡 **Đề Xuất Phương Án Sửa Đổi**: Cung cấp đoạn văn bản thay thế an toàn cho từng điều khoản bị gắn nhãn rủi ro.
- 🔒 **Zero-Persistence Privacy**: Văn bản hợp đồng chỉ được xử lý tạm thời trên bộ nhớ RAM (`ephemeral_bytes()`) và bị hủy ngay lập tức sau phân tích, không lưu vết trên đĩa cứng hay cơ sở dữ liệu.

---

## 🏗️ System Architecture

```
                               ┌────────────────────────────────────────┐
                               │         BROWSER / USER INTERFACE       │
                               │   React 18 + Vite + TypeScript (Light) │
                               └───────────────────┬────────────────────┘
                                                   │ POST /api/analyze (multipart)
                                                   ▼
                               ┌────────────────────────────────────────┐
                               │           FASTAPI BACKEND API          │
                               │   Memory-safe ephemeral bytes handling │
                               └───────────────────┬────────────────────┘
                                                   │
                ┌──────────────────────────────────┴──────────────────────────────────┐
                ▼                                                                     ▼
┌────────────────────────────────────────┐                         ┌────────────────────────────────────────┐
│      PhoBERT Multi-Label Classifier    │                         │            FAISS VECTOR INDEX          │
│   Fine-tuned vinai/phobert-base        │                         │      UTS_VLC Legal Corpus (Markdown)   │
│   Outputs 8 risk labels + probabilities│                         │      Retrieves exact Article citations │
└───────────────────┬────────────────────┘                         └───────────────────┬────────────────────┘
                    │                                                                  │
                    └──────────────────────────────────┬───────────────────────────────┘
                                                       ▼
                                       ┌────────────────────────────────┐
                                       │     CONTRACT RISK DASHBOARD    │
                                       │  Severity Score (0-100)        │
                                       │  Legal Articles + Recommendations│
                                       └────────────────────────────────┘
```

---

## 👥 Team Structure & Roles

| Member | Role | Core Responsibility |
|---|---|---|
| **AI Student 1** | Backend & ML Engineer | Huấn luyện mô hình PhoBERT (`model/train.py`), xây dựng pipeline trích xuất PDF/DOCX, thiết lập API FastAPI và FAISS vector DB. |
| **AI Student 2** | Frontend Engineer | Xây dựng giao diện React + Vite UI split-screen (`frontend/`), thiết kế bộ thẻ rủi ro, đồng bộ highlight văn bản và xuất báo cáo PDF. |
| **Law Student** | Legal Architect | Xây dựng bộ 8 nhãn rủi ro pháp lý, thẩm định dữ liệu gán nhãn, tác giả **AI Ethics Audit Report** và ma trận tuân thủ Nghị định 13/2023. |

---

## ⚖️ Risk Taxonomy (8 Categories)

Mọi nhãn rủi ro trong ContractGuard đều dựa trên **luật thực định Việt Nam**:

| ID | Label Code | Tên Tiếng Việt | Căn Cứ Pháp Lý | Điểm Rủi Ro Gốc |
|---|---|---|---|---|
| L1 | `UNFAIR_PENALTY` | Điều khoản phạt bất hợp lý | BLDS 2015 (Điều 418), LTM 2005 (Điều 301) | **85** |
| L2 | `UNILATERAL_MODIFICATION` | Sửa đổi đơn phương | BLDS 2015 (Điều 421) | **90** |
| L3 | `AMBIGUOUS_LIABILITY` | Trách nhiệm mơ hồ | BLDS 2015 (Điều 351–360) | **70** |
| L4 | `MISSING_JURISDICTION` | Thiếu điều khoản giải quyết tranh chấp | Luật Trọng tài Thương mại (Điều 5) | **65** |
| L5 | `PERSONAL_DATA_VIOLATION` | Vi phạm quyền riêng tư dữ liệu | NĐ 13/2023/NĐ-CP (Điều 9–11) | **95** *(Tối quan trọng)* |
| L6 | `EXCESSIVE_TERMINATION` | Chấm dứt hợp đồng bất lợi | BLLĐ 2019 (Điều 34–36) | **75** |
| L7 | `HIDDEN_FEE` | Phí ẩn / không minh bạch | Luật BVNTD 2023 (Điều 10) | **80** |
| L8 | `FORCE_MAJEURE_GAP` | Thiếu điều khoản bất khả kháng | BLDS 2015 (Điều 156) | **55** |

---

## 🚀 3-Layer Data Auto-Labeling Pipeline

Dữ liệu huấn luyện được chuẩn bị thông qua quy trình **Auto-Labeling 3 Lớp**, rút ngắn thời gian từ 50 giờ xuống còn **2.5 giờ**:

```
                    300 Điều khoản Hợp đồng
                               │
        ┌──────────────────────┴──────────────────────┐
        ▼                                             ▼
 [Lớp 1: Heuristics]                       [Lớp 2: OpenRouter LLM]
  Luật regex từ khóa                       Gán nhãn tự động cho
  (Phủ ~60% điều khoản)                    điều khoản phức tạp (~25%)
        │                                             │
        └──────────────────────┬──────────────────────┘
                               ▼
                   [Lớp 3: Sinh viên Luật Thẩm định]
                    Thẩm định ~45 điều khoản độ tin cậy thấp (~15%)
```

### Các lệnh thực thi gán nhãn:

```bash
# 1. Chạy Lớp 1 (Regex & Keyword Matching)
python scripts/label_heuristics.py --input data/raw_clauses.csv --output data/annotated/clauses_l1.csv

# 2. Chạy Lớp 2 (OpenRouter LLM Auto-Labeler)
set OPENROUTER_API_KEY=your_key_here
python scripts/label_with_llm.py --input data/annotated/clauses_l1.csv --output data/annotated/clauses_l2.csv

# 3. Lọc mẫu nghi ngờ cho Sinh viên Luật kiểm duyệt
python scripts/prepare_human_review.py --input data/annotated/clauses_l2.csv --output data/annotated/human_review_queue.csv
```

---

## ⚡ Model Fine-Tuning & Speed Optimizations

Mô hình `vinai/phobert-base` được fine-tune siêu tốc trong **2–4 phút** nhờ 6 kỹ thuật tối ưu hóa PyTorch & HuggingFace:

1. **Automatic Mixed Precision (FP16)**: Giảm 50% bộ nhớ VRAM, tăng tốc 2.5x trên GPU Tensor Cores.
2. **Parameter-Efficient Fine-Tuning (LoRA)**: Chỉ huấn luyện ~1.2M tham số adapter (`r=8, alpha=16`) giúp chống quên kiến thức gốc.
3. **Dynamic Batch Padding**: `DataCollatorWithPadding` đệm độ dài linh hoạt theo từng batch thay vì cố định 256 tokens.
4. **DataLoader Pin Memory**: Sử dụng `pin_memory=True` loại bỏ điểm nghẽn truyền dữ liệu CPU-to-GPU.
5. **Caching Word Tokenize**: Tiền xử lý tách từ `underthesea` trước khi huấn luyện.

---

## 💻 Getting Started & Installation

### Yêu cầu Tiền đề (Prerequisites)
- **Python**: 3.10 hoặc 3.11
- **Node.js**: 18.x trở lên & `npm`

### 1. Khởi tạo Backend (Python)

```bash
# Tạo môi trường ảo
python -m venv .venv
source .venv/bin/activate  # Trên Windows: .venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt

# Khởi chạy FastAPI Backend Server
uvicorn backend.main:app --reload --port 8000
```
Backend API sẽ sẵn sàng tại `http://localhost:8000`.

### 2. Khởi tạo Frontend (React + Vite)

```bash
# Chuyển vào thư mục frontend
cd frontend

# Cài đặt gói npm
npm install

# Khởi chạy môi trường Dev
npm run dev
```
Ứng dụng Web sẽ mở tại `http://localhost:3000`.

### 3. Huấn Luyện & Đánh Giá Mô Hình PhoBERT

```bash
# Huấn luyện mô hình PhoBERT tối ưu LoRA + FP16
python model/train.py --data_path data/annotated/clauses_annotated.csv --epochs 5 --use_lora

# Đánh giá chỉ số Macro F1 & Hamming Loss
python model/evaluate.py --model_dir model/checkpoints/best_phobert --data_path data/annotated/clauses_annotated.csv
```

---

## 📊 Evaluation Metrics & Benchmarks

| Metric | Target Baseline | Output Verification |
|---|---|---|
| **Macro F1 Score** | **$\ge 0.65$** | Evaluated on 20% held-out test split |
| **Micro F1 Score** | $\ge 0.70$ | Aggregated precision/recall |
| **Hamming Loss** | **$\le 0.15$** | Multi-label classification error rate |
| **Analysis Latency (5-page PDF)** | **$< 8$ seconds** | End-to-end API response time |
| **Privacy Compliance** | **100% Pass** | Memory zeroing assertion test (`test_privacy.py`) |

---

## 🔒 Privacy & Legal Compliance

ContractGuard cam kết tuân thủ nghiêm ngặt **Nghị định 13/2023/NĐ-CP** về Bảo vệ Dữ liệu Cá nhân:
- **Điều 9 (Mục đích rõ ràng)**: Thông báo bảo mật ngay tại giao diện tải file.
- **Điều 10 (Giới hạn lưu trữ)**: Không lưu vết file hợp đồng trên bất kỳ đĩa cứng hay cơ sở dữ liệu nào (`ephemeral_bytes()`).
- **Miễn trừ trách nhiệm**: "ContractGuard cung cấp thông tin cảnh báo rủi ro, KHÔNG thay thế tư vấn pháp lý chuyên nghiệp."

---

## 📁 Project Structure

```
contractguard/
├── backend/
│   ├── main.py               # Application factory create_app()
│   ├── schemas/              # Request & Response models (ApiResponse envelope)
│   └── core/                 # Config & Privacy (ephemeral_bytes manager)
│
├── model/
│   ├── train.py              # PhoBERT fine-tuning với LoRA + FP16
│   ├── evaluate.py           # Tính Macro F1, Micro F1, Hamming Loss
│   └── checkpoints/          # Lưu trữ trọng số mô hình
│
├── frontend/                 # React 18 + Vite + TypeScript (Light Theme UI)
│   ├── src/
│   │   ├── components/       # DocumentViewer, RiskPanel, SeverityGauge, UploadZone
│   │   ├── hooks/            # useContractAnalysis
│   │   ├── data/             # sampleContracts (Preloaded demo data)
│   │   ├── styles/           # index.css (Vanilla CSS Tokens)
│   │   └── types/            # analysis.ts
│   ├── package.json
│   └── vite.config.ts
│
├── data/
│   ├── raw_contracts/        # Hợp đồng thô (gitignored)
│   └── annotated/            # clauses_annotated.csv (Ground truth)
│
├── scripts/
│   ├── label_heuristics.py   # Layer 1: Rule Engine keyword matching
│   ├── label_with_llm.py     # Layer 2: OpenRouter API Auto-Labeler
│   └── prepare_human_review.py # Layer 3: Lọc mẫu cho Sinh viên Luật
│
├── legal/
│   ├── risk_taxonomy.md      # 8 nhãn rủi ro + Căn cứ pháp lý
│   └── annotation_guidelines.md # Hướng dẫn thẩm định cho Luật
│
├── requirements.txt          # Python dependencies
├── .gitignore                # Production ignore settings
└── README.md                 # Project documentation
```

---

## 📜 License

Dự án ContractGuard được phát hành theo giấy phép [Apache 2.0 License](LICENSE). Trọng số PhoBERT thuộc bản quyền của VinAI Research (Apache 2.0).

---

*ContractGuard — Kiến tạo sự an toàn pháp lý cho mọi hợp đồng Việt Nam.*
