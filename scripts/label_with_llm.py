#!/usr/bin/env python3
"""
Layer 2 Data Auto-Labeling Engine (OpenRouter LLM API)
ContractGuard — Sáng tạo AI 2026

Uses OpenRouter API (e.g. google/gemini-flash-1.5 or openai/gpt-4o-mini)
to classify contract clauses not confidentially labeled by Layer 1.
"""

import argparse
import os
import json
import urllib.request
import pandas as pd
from typing import Dict, List, Any

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-4o-mini"

SYSTEM_PROMPT = """Bạn là một chuyên gia pháp lý và AI annotator cho hợp đồng Việt Nam.
Nhiệm vụ của bạn là phân tích điều khoản hợp đồng và gán các nhãn rủi ro theo 8 danh mục sau:

1. L1_UNFAIR_PENALTY: Điều khoản phạt vi phạm bất hợp lý (>8% hoặc phạt quá nặng).
2. L2_UNILATERAL_MODIFICATION: Quyền sửa đổi/hủy bỏ đơn phương từ một bên.
3. L3_AMBIGUOUS_LIABILITY: Trách nhiệm mơ hồ, quy trách nhiệm trong mọi trường hợp.
4. L4_MISSING_JURISDICTION: Thiếu điều khoản giải quyết tranh chấp / cơ quan tài phán.
5. L5_PERSONAL_DATA_VIOLATION: Vi phạm dữ liệu cá nhân theo NĐ 13/2023/NĐ-CP.
6. L6_EXCESSIVE_TERMINATION: Chấm dứt hợp đồng bất lợi, cho nghỉ việc ngay lập tức.
7. L7_HIDDEN_FEE: Phí ẩn, chi phí phụ không minh bạch.
8. L8_FORCE_MAJEURE_GAP: Thiếu hoặc loại bỏ bất khả kháng bất hợp lý.

Trả về định dạng JSON DUY NHẤT như sau:
{
  "labels": {
    "L1_UNFAIR_PENALTY": 0,
    "L2_UNILATERAL_MODIFICATION": 1,
    "L3_AMBIGUOUS_LIABILITY": 0,
    "L4_MISSING_JURISDICTION": 0,
    "L5_PERSONAL_DATA_VIOLATION": 0,
    "L6_EXCESSIVE_TERMINATION": 0,
    "L7_HIDDEN_FEE": 0,
    "L8_FORCE_MAJEURE_GAP": 0
  },
  "confidence": 0.85,
  "reasoning": "Giải thích ngắn gọn lý do gán nhãn"
}"""

def call_openrouter(clause_text: str, api_key: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    """Queries OpenRouter API for multi-label classification."""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Phân tích điều khoản sau:\n\"{clause_text}\""}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.1
    }
    
    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "HTTP-Referer": "https://contractguard.vn",
        "X-Title": "ContractGuard Auto-Labeler"
    }

    req = urllib.request.Request(
        OPENROUTER_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res_body = response.read().decode("utf-8")
            data = json.loads(res_body)
            content = data["choices"][0]["message"]["content"]
            return json.loads(content)
    except Exception as e:
        print(f"API Error for clause: {e}")
        return {
            "labels": {k: 0 for k in [
                "L1_UNFAIR_PENALTY", "L2_UNILATERAL_MODIFICATION", "L3_AMBIGUOUS_LIABILITY",
                "L4_MISSING_JURISDICTION", "L5_PERSONAL_DATA_VIOLATION", "L6_EXCESSIVE_TERMINATION",
                "L7_HIDDEN_FEE", "L8_FORCE_MAJEURE_GAP"
            ]},
            "confidence": 0.0,
            "reasoning": f"Error calling API: {str(e)}"
        }

def main():
    parser = argparse.ArgumentParser(description="Layer 2 OpenRouter Data Auto-Labeling")
    parser.add_argument("--input", type=str, required=True, help="Input CSV file from Layer 1")
    parser.add_argument("--output", type=str, required=True, help="Output CSV file for Layer 2")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="OpenRouter model name")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    # Fallback: check for .env file in root directory
    if not api_key and os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("OPENROUTER_API_KEY="):
                    api_key = line.strip().split("=", 1)[1].strip('"\'')
                    break

    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY not found!")
        print("Please place your API key in a `.env` file at the project root:")
        print("  OPENROUTER_API_KEY=sk-or-v1-your-key-here")
        print("Or set it in your terminal:")
        print("  set OPENROUTER_API_KEY=sk-or-v1-your-key-here  (Windows)")
        print("  export OPENROUTER_API_KEY=sk-or-v1-your-key-here (Linux/Mac)")
        return

    df = pd.read_csv(args.input)
    print(f"Processing {len(df)} clauses with OpenRouter model '{args.model}'...")

    results = []
    for idx, row in df.iterrows():
        # If Layer 1 high confidence, skip LLM call to save time and API quota
        if row.get("annotator") == "RULE_ENGINE" and row.get("confidence_score", 0) >= 0.85:
            results.append(row.to_dict())
            continue

        clause_text = str(row.get("clause_text", ""))
        llm_out = call_openrouter(clause_text, api_key, model=args.model)
        
        row_dict = row.to_dict()
        row_dict.update(llm_out.get("labels", {}))
        row_dict["confidence_score"] = llm_out.get("confidence", 0.70)
        row_dict["annotator"] = "OPENROUTER_LLM"
        results.append(row_dict)
        print(f"[{idx+1}/{len(df)}] Labeled clause {row.get('clause_id')}")

    res_df = pd.DataFrame(results)
    res_df.to_csv(args.output, index=False)
    print(f"Layer 2 auto-labeling complete. Saved to {args.output}")

if __name__ == "__main__":
    main()
