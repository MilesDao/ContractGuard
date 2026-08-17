#!/usr/bin/env python3
"""
📥 ContractGuard — Vietnamese Legal Corpus Downloader
Downloads `undertheseanlp/UTS_VLC` dataset from HuggingFace
and saves it locally to `data/legal_corpus/` for FAISS vector indexing.
"""

import os
from datasets import load_dataset

def main():
    target_dir = "data/legal_corpus"
    os.makedirs(target_dir, exist_ok=True)
    
    print("="*60)
    print("📥 DOWNLOADING VIETNAMESE LEGAL CORPUS (undertheseanlp/UTS_VLC)")
    print("="*60)
    
    try:
        # Load dataset from HuggingFace
        print("Fetching dataset from HuggingFace hub...")
        dataset = load_dataset("undertheseanlp/UTS_VLC")
        
        print(f"Dataset successfully downloaded! Splits available: {list(dataset.keys())}")
        
        # Save to local disk
        save_path = os.path.join(target_dir, "uts_vlc")
        dataset.save_to_disk(save_path)
        print(f"✅ Saved HuggingFace dataset to: {save_path}")

        # Also export as clean readable text / json for FAISS indexing
        for split_name in dataset.keys():
            df = dataset[split_name].to_pandas()
            csv_path = os.path.join(target_dir, f"legal_corpus_{split_name}.csv")
            df.to_csv(csv_path, index=False, encoding="utf-8-sig")
            print(f"📄 Exported {len(df)} legal documents ({split_name}) to: {csv_path}")

    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        print("Creating fallback legal statutory offline files...")
        
        # Create minimal verified legal corpus file for offline RAG indexing
        offline_statutes = [
            {
                "doc_id": "BLDS_2015_418",
                "doc_type": "BỘ LUẬT",
                "title": "Bộ luật Dân sự 2015 — Điều 418. Thỏa thuận phạt vi phạm",
                "content": "Phạt vi phạm là sự thỏa thuận giữa các bên trong hợp đồng, theo đó bên vi phạm nghĩa vụ phải nộp một khoản tiền cho bên bị vi phạm. Mức phạt vi phạm do các bên thỏa thuận, trừ trường hợp luật liên quan có quy định khác."
            },
            {
                "doc_id": "LTM_2005_301",
                "doc_type": "LUẬT",
                "title": "Luật Thương mại 2005 — Điều 301. Mức phạt vi phạm",
                "content": "Mức phạt đối với vi phạm nghĩa vụ hợp đồng hoặc tổng mức phạt đối với nhiều vi phạm do các bên thỏa thuận trong hợp đồng, nhưng không quá 8% giá trị phần nghĩa vụ hợp đồng bị vi phạm, trừ trường hợp quy định tại Điều 266 của Luật này."
            },
            {
                "doc_id": "BLLD_2019_029",
                "doc_type": "BỘ LUẬT",
                "title": "Bộ luật Lao động 2019 — Điều 29. Chuyển người lao động làm công việc khác so với hợp đồng lao động",
                "content": "Khi gặp khó khăn đột xuất do thiên tai, hỏa hoạn, dịch bệnh nguy hiểm, người sử dụng lao động được quyền tạm thời chuyển người lao động làm công việc khác so với hợp đồng lao động nhưng không được quá 60 ngày làm việc cộng dồn trong 01 năm và phải báo trước ít nhất 03 ngày làm việc."
            },
            {
                "doc_id": "ND13_2023_009",
                "doc_type": "NGHỊ ĐỊNH",
                "title": "Nghị định 13/2023/NĐ-CP — Điều 9. Quyền của chủ thể dữ liệu",
                "content": "Chủ thể dữ liệu có quyền được biết về hoạt động xử lý dữ liệu cá nhân của mình, trừ trường hợp luật có quy định khác. Chủ thể dữ liệu có quyền đồng ý hoặc không đồng ý cho phép xử lý dữ liệu cá nhân của mình."
            }
        ]
        
        import pandas as pd
        df = pd.DataFrame(offline_statutes)
        csv_path = os.path.join(target_dir, "legal_corpus_train.csv")
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"✅ Saved offline legal corpus sample to: {csv_path}")

if __name__ == "__main__":
    main()
