#!/usr/bin/env python3
"""
⚡ ContractGuard — 3-Layer Auto-Labeling Pipeline Runner
Orchestrates Layer 1 (Heuristics) -> Layer 2 (OpenRouter LLM) -> Layer 3 (Human Audit Filter)

Usage:
    python scripts/run_auto_labeling.py --input data/raw_clauses.csv
"""

import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="ContractGuard 3-Layer Auto-Labeling Master Runner")
    parser.add_argument("--input", type=str, default="data/annotated/clauses_annotated.csv", help="Input raw clauses CSV")
    parser.add_argument("--output_dir", type=str, default="data/annotated", help="Directory to save pipeline outputs")
    parser.add_argument("--model", type=str, default="google/gemini-flash-1.5", help="OpenRouter model name for Layer 2")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"❌ Input file '{args.input}' does not exist.")
        return

    os.makedirs(args.output_dir, exist_ok=True)
    l1_output = os.path.join(args.output_dir, "clauses_l1.csv")
    l2_output = os.path.join(args.output_dir, "clauses_l2.csv")
    l3_output = os.path.join(args.output_dir, "human_review_queue.csv")

    print("\n" + "="*60)
    print("🛡️ RUNNING 3-LAYER DATA AUTO-LABELING PIPELINE")
    print("="*60)

    # -------------------------------------------------------------
    # Layer 1: Rule Engine
    # -------------------------------------------------------------
    print("\n[LAYER 1] Running Regex & Keyword Heuristic Engine...")
    cmd_l1 = [sys.executable, "scripts/label_heuristics.py", "--input", args.input, "--output", l1_output]
    ret_l1 = subprocess.run(cmd_l1)
    if ret_l1.returncode != 0:
        print("❌ Layer 1 failed.")
        return

    # -------------------------------------------------------------
    # Layer 2: OpenRouter API LLM
    # -------------------------------------------------------------
    print("\n[LAYER 2] Running OpenRouter LLM Auto-Labeler...")
    cmd_l2 = [sys.executable, "scripts/label_with_llm.py", "--input", l1_output, "--output", l2_output, "--model", args.model]
    ret_l2 = subprocess.run(cmd_l2)
    if ret_l2.returncode != 0:
        print("❌ Layer 2 failed.")
        return

    # -------------------------------------------------------------
    # Layer 3: Human Audit Filter
    # -------------------------------------------------------------
    print("\n[LAYER 3] Filtering Low-Confidence Clauses for Law Student Audit...")
    cmd_l3 = [sys.executable, "scripts/prepare_human_review.py", "--input", l2_output, "--output", l3_output]
    ret_l3 = subprocess.run(cmd_l3)
    if ret_l3.returncode != 0:
        print("❌ Layer 3 failed.")
        return

    print("\n" + "="*60)
    print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"  • L1 Labeled Data: {l1_output}")
    print(f"  • L2 Labeled Data: {l2_output}")
    print(f"  • L3 Human Queue:  {l3_output}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
