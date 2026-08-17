#!/usr/bin/env python3
"""
📊 ContractGuard — Model Evaluation & Metrics Report Script
Evaluates trained PhoBERT classifier against test set and outputs Macro F1, Micro F1, and per-label metrics.
"""

import argparse
import os
import torch
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification

LABEL_COLS = [
    "L1_UNFAIR_PENALTY",
    "L2_UNILATERAL_MODIFICATION",
    "L3_AMBIGUOUS_LIABILITY",
    "L4_MISSING_JURISDICTION",
    "L5_PERSONAL_DATA_VIOLATION",
    "L6_EXCESSIVE_TERMINATION",
    "L7_HIDDEN_FEE",
    "L8_FORCE_MAJEURE_GAP"
]

def evaluate_model(model_dir: str, data_path: str):
    print(f"Loading model from {model_dir}...")
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    model.eval()

    if torch.cuda.is_available():
        model = model.cuda()

    df = pd.read_csv(data_path)
    texts = df["tokenized_text"].fillna(df["clause_text"]).tolist()
    labels = df[LABEL_COLS].values

    all_preds = []

    print(f"Evaluating {len(df)} test clauses...")
    with torch.no_grad():
        for text in texts:
            inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            outputs = model(**inputs)
            probs = torch.sigmoid(outputs.logits).cpu().numpy()[0]
            preds = (probs >= 0.5).astype(int)
            all_preds.append(preds)

    all_preds = np.array(all_preds)

    print("\n" + "="*50)
    print("📈 EVALUATION METRICS REPORT")
    print("="*50)

    tp = np.sum((all_preds == 1) & (labels == 1), axis=0)
    fp = np.sum((all_preds == 1) & (labels == 0), axis=0)
    fn = np.sum((all_preds == 0) & (labels == 1), axis=0)

    precision = np.divide(tp, tp + fp + 1e-7)
    recall = np.divide(tp, tp + fn + 1e-7)
    f1 = 2 * (precision * recall) / (precision + recall + 1e-7)

    metrics_df = pd.DataFrame({
        "Label": LABEL_COLS,
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1
    })

    print(metrics_df.to_string(index=False))

    macro_f1 = np.mean(f1)
    micro_f1 = 2 * np.sum(tp) / (2 * np.sum(tp) + np.sum(fp) + np.sum(fn) + 1e-7)
    hamming_loss = np.mean(all_preds != labels)

    print("\n" + "-"*50)
    print(f"🎯 Macro F1:      {macro_f1:.4f} (Target: ≥ 0.65)")
    print(f"🎯 Micro F1:      {micro_f1:.4f}")
    print(f"🎯 Hamming Loss:  {hamming_loss:.4f} (Target: ≤ 0.15)")
    print("-"*50 + "\n")

def main():
    parser = argparse.ArgumentParser(description="PhoBERT Model Evaluator")
    parser.add_argument("--model_dir", type=str, default="model/checkpoints/best_phobert", help="Path to model checkpoint")
    parser.add_argument("--data_path", type=str, default="data/annotated/clauses_annotated.csv", help="Test dataset CSV")
    args = parser.parse_args()

    if not os.path.exists(args.model_dir):
        print(f"Error: Model checkpoint directory '{args.model_dir}' not found.")
        return
    if not os.path.exists(args.data_path):
        print(f"Error: Test dataset '{args.data_path}' not found.")
        return

    evaluate_model(args.model_dir, args.data_path)

if __name__ == "__main__":
    main()
