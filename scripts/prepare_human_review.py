#!/usr/bin/env python3
"""
Layer 3 Human Review Filter Engine
ContractGuard — Sáng tạo AI 2026

Filters clauses with low confidence (< 0.70) or uncertain auto-labels
so the Law Student reviews only the necessary samples (~15% of dataset).
"""

import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Layer 3 Human Review Filter")
    parser.add_argument("--input", type=str, required=True, help="Input CSV file from Layer 2")
    parser.add_argument("--output", type=str, required=True, help="Output CSV for human review queue")
    parser.add_argument("--threshold", type=float, default=0.70, help="Confidence threshold below which human review is required")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    print(f"Filtering dataset of {len(df)} clauses...")

    # Filter condition: confidence < threshold OR annotator == UNLABELED
    needs_review = df[(df["confidence_score"] < args.threshold) | (df["annotator"] == "UNLABELED")].copy()

    needs_review.to_csv(args.output, index=False)
    print(f"Found {len(needs_review)} clauses requiring human review ({len(needs_review)/len(df)*100:.1f}%).")
    print(f"Saved review queue to {args.output}")

if __name__ == "__main__":
    main()
