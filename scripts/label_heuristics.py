#!/usr/bin/env python3
"""
Layer 1 Data Auto-Labeling Engine (Keyword & Regex Rules)
ContractGuard — Sáng tạo AI 2026

Flags obvious Vietnamese legal risk clauses with high precision (~60% coverage).
"""

import argparse
import re
import pandas as pd
from typing import Dict, List, Tuple

# Risk Label Regex Patterns
PATTERNS: Dict[str, List[str]] = {
    "L1_UNFAIR_PENALTY": [
        r"phạt\s+(?:vi\s+phạm\s+)?(?:quá\s+)?(?:[8-9]|\d{2,})%",
        r"bồi\s+thường\s+gấp\s+\d+",
        r"chịu\s+phạt\s+\d+%",
        r"mất\s+toàn\s+bộ\s+tiền\s+cọc",
        r"bồi\s+thường\s+\d+%\s+chi\s+phí"
    ],
    "L2_UNILATERAL_MODIFICATION": [
        r"bên\s+[ab]\s+có\s+quyền\s+đơn\s+phương",
        r"tự\s+động\s+điều\s+chỉnh",
        r"thay\s+đổi\s+điều\s+khoản\s+mà\s+không\s+cần\s+báo",
        r"quyết\s+định\s+của\s+bên\s+[ab]\s+là\s+quyết\s+định\s+cuối\s+cùng"
    ],
    "L3_AMBIGUOUS_LIABILITY": [
        r"chịu\s+trách\s+nhiệm\s+trong\s+mọi\s+trường\s+hợp",
        r"mọi\s+thiệt\s+hại\s+phát\s+sinh",
        r"không\s+phụ\s+thuộc\s+vào\s+yếu\s+tố\s+lỗi",
        r"theo\s+quyết\s+định\s+của\s+bên"
    ],
    "L4_MISSING_JURISDICTION": [
        # Check negative: if missing both court and arbitration mentions
    ],
    "L5_PERSONAL_DATA_VIOLATION": [
        r"toàn\s+quyền\s+thu\s+thập.*dữ\s+liệu\s+cá\s+nhân",
        r"chia\s+sẻ.*thông\s+tin\s+cá\s+nhân.*thứ\s+ba",
        r"không\s+cần\s+thông\s+báo.*dữ\s+liệu",
        r"sử\s+dụng\s+thông\s+tin.*cho\s+mục\s+đích\s+khác"
    ],
    "L6_EXCESSIVE_TERMINATION": [
        r"cho\s+nghỉ\s+việc\s+ngay\s+lập\s+tức",
        r"chấm\s+dứt\s+không\s+cần\s+lý\s+do",
        r"không\s+thanh\s+toán\s+trợ\s+cấp",
        r"chấm\s+dứt\s+hợp\s+đồng\s+ngay\s+mà\s+không\s+báo"
    ],
    "L7_HIDDEN_FEE": [
        r"chi\s+phí\s+phát\s+sinh\s+khác",
        r"theo\s+phụ\s+lục\s+phí.*không\s+nêu\s+trực\s+tiếp",
        r"phí\s+bổ\s+sung\s+theo\s+quy\s+định\s+riêng"
    ],
    "L8_FORCE_MAJEURE_GAP": [
        r"vẫn\s+phải\s+thanh\s+toán.*thiên\s+tai",
        r"không\s+miễn\s+trừ.*bất\s+khả\s+kháng"
    ]
}

def apply_heuristics(clause_text: str) -> Tuple[Dict[str, int], float]:
    """Applies rule-based keyword matching to a clause."""
    text_lower = clause_text.lower()
    labels = {
        "L1_UNFAIR_PENALTY": 0,
        "L2_UNILATERAL_MODIFICATION": 0,
        "L3_AMBIGUOUS_LIABILITY": 0,
        "L4_MISSING_JURISDICTION": 0,
        "L5_PERSONAL_DATA_VIOLATION": 0,
        "L6_EXCESSIVE_TERMINATION": 0,
        "L7_HIDDEN_FEE": 0,
        "L8_FORCE_MAJEURE_GAP": 0,
    }
    
    matches_count = 0
    for label, pattern_list in PATTERNS.items():
        for pat in pattern_list:
            if re.search(pat, text_lower):
                labels[label] = 1
                matches_count += 1
                break
                
    # Specific check for missing jurisdiction clause
    if "tòa án" not in text_lower and "trọng tài" not in text_lower and "giải quyết tranh chấp" not in text_lower:
        # If the clause talks about disputes but misses jurisdiction
        if "tranh chấp" in text_lower or "khiếu nại" in text_lower:
            labels["L4_MISSING_JURISDICTION"] = 1
            matches_count += 1

    confidence = 0.90 if matches_count > 0 else 0.50
    return labels, confidence

def main():
    parser = argparse.ArgumentParser(description="Layer 1 Heuristics Data Labeling")
    parser.add_argument("--input", type=str, required=True, help="Input CSV file with raw clauses")
    parser.add_argument("--output", type=str, required=True, help="Output CSV file for L1 labeled data")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    print(f"Loaded {len(df)} clauses from {args.input}")

    results = []
    for _, row in df.iterrows():
        clause = str(row.get("clause_text", ""))
        labels, conf = apply_heuristics(clause)
        row_dict = row.to_dict()
        row_dict.update(labels)
        row_dict["confidence_score"] = conf
        row_dict["annotator"] = "RULE_ENGINE" if conf > 0.50 else "UNLABELED"
        results.append(row_dict)

    res_df = pd.DataFrame(results)
    res_df.to_csv(args.output, index=False)
    print(f"Layer 1 auto-labeling completed. Saved to {args.output}")

if __name__ == "__main__":
    main()
