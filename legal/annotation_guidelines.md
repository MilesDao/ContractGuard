# 📑 ContractGuard — Data Annotation Guidelines for Legal Review

> **Instructions for Law Student & AI Annotators**
> Goal: Annotate contract clauses consistently for fine-tuning `vinai/phobert-base` multi-label classifier.

---

## 1. Multi-Label Classification Rules
- Each clause can have **0, 1, or multiple risk labels** (e.g. a clause can be both `UNFAIR_PENALTY` and `UNILATERAL_MODIFICATION`).
- If a clause is standard legal boilerplates without unfair terms, set all label flags to `0`.

---

## 2. 3-Layer Auto-Labeling Workflow

### Layer 1: Rule Engine Run
Run the Python keyword script to flag obvious clauses:
```bash
python scripts/label_heuristics.py --input data/raw_clauses.csv --output data/annotated/clauses_l1.csv
```

### Layer 2: OpenRouter LLM Auto-Labeling
Run the LLM classification for unflagged/complex clauses:
```bash
python scripts/label_with_llm.py --input data/annotated/clauses_l1.csv --output data/annotated/clauses_l2.csv
```

### Layer 3: Human Law Student Audit
Filter clauses needing human validation:
```bash
python scripts/prepare_human_review.py --input data/annotated/clauses_l2.csv --output data/annotated/human_review_queue.csv
```

The Law Student opens `human_review_queue.csv` in Excel or Google Sheets, reviews the flags, updates `0` or `1`, sets `confidence_score = 1.0`, and sets `annotator = LAW_STUDENT`.

---

## 3. Standard CSV Column Format

| Column | Type | Example |
|---|---|---|
| `clause_id` | string | `HDLD_01_C05` |
| `contract_type` | string | `LABOR` |
| `clause_text` | string | `Bên A có quyền đơn phương chấm dứt hợp đồng và phạt 20% tiền lương.` |
| `tokenized_text` | string | `Bên_A có quyền đơn_phương chấm_dứt hợp_đồng và phạt 20% tiền_lương .` |
| `L1_UNFAIR_PENALTY` | int (0/1) | `1` |
| `L2_UNILATERAL_MODIFICATION` | int (0/1) | `0` |
| `L3_AMBIGUOUS_LIABILITY` | int (0/1) | `0` |
| `L4_MISSING_JURISDICTION` | int (0/1) | `0` |
| `L5_PERSONAL_DATA_VIOLATION` | int (0/1) | `0` |
| `L6_EXCESSIVE_TERMINATION` | int (0/1) | `1` |
| `L7_HIDDEN_FEE` | int (0/1) | `0` |
| `L8_FORCE_MAJEURE_GAP` | int (0/1) | `0` |
| `confidence_score` | float | `1.0` |
| `annotator` | string | `LAW_STUDENT` |

---

## 4. Key Edge Cases & Legal Precedents

1. **Penalty vs Compensation**: Penalty (`Phạt vi phạm`) without proving damages is capped at 8% in commercial contracts. Compensation for actual damages (`Bồi thường thiệt hại`) is allowed, but clauses demanding arbitrary high fixed damages without proof are labeled `UNFAIR_PENALTY`.
2. **Personal Data Consent**: A blanket consent clause stating "User agrees to share data with third parties" without specifying purpose or data types is labeled `PERSONAL_DATA_VIOLATION` under Decree 13/2023/NĐ-CP Art. 9.
3. **Probation in Labor Contracts**: Probation periods exceeding statutory limits (e.g. 180 days for standard staff) or paying less than 85% salary fall under `EXCESSIVE_TERMINATION` / `UNFAIR_PENALTY`.
