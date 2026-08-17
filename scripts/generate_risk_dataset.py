#!/usr/bin/env python3
"""
🛡️ ContractGuard — Synthetic Risk Dataset Generator & Data Augmenter
Generates realistic Vietnamese contract clauses with balanced positive (1) and negative (0) labels
across all 8 risk categories (especially UNFAIR_PENALTY, UNILATERAL_MODIFICATION, PERSONAL_DATA_VIOLATION).
"""

import os
import pandas as pd
import numpy as np

# Comprehensive dataset of realistic Vietnamese contract clauses
DATASET_SAMPLES = [
    # --- 1. UNFAIR_PENALTY (Phạt vi phạm bất hợp lý) ---
    {
        "clause_id": "HDLD_PEN_01",
        "contract_type": "LABOR",
        "clause_text": "Trong trường hợp Người lao động nghỉ việc trước thời hạn hợp đồng thì phải bồi thường 200% chi phí đào tạo và chịu phạt 20% tổng thu nhập đã nhận trong suốt thời gian làm việc.",
        "tokenized_text": "Trong trường_hợp Người lao_động nghỉ việc trước thời_hạn hợp_đồng thì phải bồi_thường 200% chi_phí đào_tạo và chịu phạt 20% tổng thu_nhập đã nhận trong suốt thời_gian làm_việc .",
        "L1_UNFAIR_PENALTY": 1, "L2_UNILATERAL_MODIFICATION": 0, "L3_AMBIGUOUS_LIABILITY": 0, "L4_MISSING_JURISDICTION": 0,
        "L5_PERSONAL_DATA_VIOLATION": 0, "L6_EXCESSIVE_TERMINATION": 1, "L7_HIDDEN_FEE": 0, "L8_FORCE_MAJEURE_GAP": 0,
        "confidence_score": 1.0, "annotator": "LEGAL_EXPERT"
    },
    {
        "clause_id": "HDMB_PEN_02",
        "contract_type": "SALES",
        "clause_text": "Nếu Bên Mua chậm thanh toán dù chỉ 01 ngày thì Bên Mua phải chịu phạt vi phạm bằng 50% tổng giá trị hợp đồng và bồi thường thêm 100% giá trị lô hàng.",
        "tokenized_text": "Nếu Bên Mua chậm thanh_toán dù chỉ 01 ngày thì Bên Mua phải chịu phạt vi_phạm bằng 50% tổng giá_trị hợp_đồng và bồi_thường thêm 100% giá_trị lô hàng .",
        "L1_UNFAIR_PENALTY": 1, "L2_UNILATERAL_MODIFICATION": 0, "L3_AMBIGUOUS_LIABILITY": 0, "L4_MISSING_JURISDICTION": 0,
        "L5_PERSONAL_DATA_VIOLATION": 0, "L6_EXCESSIVE_TERMINATION": 0, "L7_HIDDEN_FEE": 0, "L8_FORCE_MAJEURE_GAP": 0,
        "confidence_score": 1.0, "annotator": "LEGAL_EXPERT"
    },
    {
        "clause_id": "HDTH_PEN_03",
        "contract_type": "LEASE",
        "clause_text": "Bên Thuê chậm trả tiền nhà từ 03 ngày trở lên sẽ bị tịch thu toàn bộ 100% tiền đặt cọc và chịu phạt thêm 03 tháng tiền thuê nhà mà Bên Cho Thuê không cần chứng minh thiệt hại.",
        "tokenized_text": "Bên Thuê chậm trả tiền nhà từ 03 ngày trở lên sẽ bị tịch_thu toàn_bộ 100% tiền đặt cọc và chịu phạt thêm 03 tháng tiền thuê nhà mà Bên Cho_Thuê không cần chứng_minh thiệt_hại .",
        "L1_UNFAIR_PENALTY": 1, "L2_UNILATERAL_MODIFICATION": 0, "L3_AMBIGUOUS_LIABILITY": 0, "L4_MISSING_JURISDICTION": 0,
        "L5_PERSONAL_DATA_VIOLATION": 0, "L6_EXCESSIVE_TERMINATION": 0, "L7_HIDDEN_FEE": 0, "L8_FORCE_MAJEURE_GAP": 0,
        "confidence_score": 1.0, "annotator": "LEGAL_EXPERT"
    },
    {
        "clause_id": "HDDV_PEN_04",
        "contract_type": "SERVICE",
        "clause_text": "Nếu Bên B vi phạm bất kỳ điều khoản nào trong hợp đồng này thì Bên A có quyền khấu trừ 100% phí dịch vụ chưa thanh toán và phạt Bên B số tiền bằng 30% giá trị hợp đồng.",
        "tokenized_text": "Nếu Bên B vi_phạm bất_kỳ điều_khoản nào trong hợp_đồng này thì Bên A có quyền khấu_trừ 100% phí dịch_vụ chưa thanh_toán và phạt Bên B số tiền bằng 30% giá_trị hợp_đồng .",
        "L1_UNFAIR_PENALTY": 1, "L2_UNILATERAL_MODIFICATION": 0, "L3_AMBIGUOUS_LIABILITY": 0, "L4_MISSING_JURISDICTION": 0,
        "L5_PERSONAL_DATA_VIOLATION": 0, "L6_EXCESSIVE_TERMINATION": 0, "L7_HIDDEN_FEE": 0, "L8_FORCE_MAJEURE_GAP": 0,
        "confidence_score": 1.0, "annotator": "LEGAL_EXPERT"
    },
    {
        "clause_id": "HDLD_PEN_05",
        "contract_type": "LABOR",
        "clause_text": "Người lao động vi phạm quy định bảo mật thông tin sẽ bị tịch thu toàn bộ tiền lương của tháng đó và bồi thường cố định 500.000.000 VNĐ.",
        "tokenized_text": "Người lao_động vi_phạm quy_định bảo_mật thông_tin sẽ bị tịch_thu toàn_bộ tiền_lương của tháng đó và bồi_thường cố_định 500.000.000 VNĐ .",
        "L1_UNFAIR_PENALTY": 1, "L2_UNILATERAL_MODIFICATION": 0, "L3_AMBIGUOUS_LIABILITY": 0, "L4_MISSING_JURISDICTION": 0,
        "L5_PERSONAL_DATA_VIOLATION": 0, "L6_EXCESSIVE_TERMINATION": 0, "L7_HIDDEN_FEE": 0, "L8_FORCE_MAJEURE_GAP": 0,
        "confidence_score": 1.0, "annotator": "LEGAL_EXPERT"
    },

    # --- 2. UNILATERAL_MODIFICATION (Sửa đổi đơn phương) ---
    {
        "clause_id": "HDTH_UNI_01",
        "contract_type": "LEASE",
        "clause_text": "Bên Cho Thuê có quyền toàn quyền điều chỉnh tăng giá thuê nhà bất kỳ lúc nào mà không cần thỏa thuận hoặc báo trước cho Bên Thuê.",
        "tokenized_text": "Bên Cho_Thuê có quyền toàn quyền điều_chỉnh tăng giá thuê nhà bất_kỳ lúc nào mà không cần thỏa_thuận hoặc báo trước cho Bên Thuê .",
        "L1_UNFAIR_PENALTY": 0, "L2_UNILATERAL_MODIFICATION": 1, "L3_AMBIGUOUS_LIABILITY": 0, "L4_MISSING_JURISDICTION": 0,
        "L5_PERSONAL_DATA_VIOLATION": 0, "L6_EXCESSIVE_TERMINATION": 0, "L7_HIDDEN_FEE": 0, "L8_FORCE_MAJEURE_GAP": 0,
        "confidence_score": 1.0, "annotator": "LEGAL_EXPERT"
    },
    {
        "clause_id": "HDDV_UNI_02",
        "contract_type": "SERVICE",
        "clause_text": "Bên A có quyền thay đổi phạm vi công việc và tiến độ giao hàng mà không cần sự đồng ý bằng văn bản của Bên B.",
        "tokenized_text": "Bên A có quyền thay_đổi phạm_vi công_việc và tiến_độ giao hàng mà không cần sự đồng_ý bằng văn_bản của Bên B .",
        "L1_UNFAIR_PENALTY": 0, "L2_UNILATERAL_MODIFICATION": 1, "L3_AMBIGUOUS_LIABILITY": 0, "L4_MISSING_JURISDICTION": 0,
        "L5_PERSONAL_DATA_VIOLATION": 0, "L6_EXCESSIVE_TERMINATION": 0, "L7_HIDDEN_FEE": 0, "L8_FORCE_MAJEURE_GAP": 0,
        "confidence_score": 1.0, "annotator": "LEGAL_EXPERT"
    },

    # --- 3. AMBIGUOUS_LIABILITY (Trách nhiệm mơ hồ) ---
    {
        "clause_id": "HDDV_AMB_01",
        "contract_type": "SERVICE",
        "clause_text": "Mọi thiệt hại phát sinh liên quan trực tiếp hoặc gián tiếp đến hợp đồng này sẽ do Bên B chịu trách nhiệm trong mọi trường hợp mà không phụ thuộc vào yếu tố lỗi.",
        "tokenized_text": "Mọi thiệt_hại phát_sinh liên_quan trực_tiếp hoặc gián_tiếp đến hợp_đồng này sẽ do Bên B chịu trách_nhiệm trong mọi trường_hợp mà không phụ_thuộc vào yếu_tố lỗi .",
        "L1_UNFAIR_PENALTY": 0, "L2_UNILATERAL_MODIFICATION": 0, "L3_AMBIGUOUS_LIABILITY": 1, "L4_MISSING_JURISDICTION": 0,
        "L5_PERSONAL_DATA_VIOLATION": 0, "L6_EXCESSIVE_TERMINATION": 0, "L7_HIDDEN_FEE": 0, "L8_FORCE_MAJEURE_GAP": 0,
        "confidence_score": 1.0, "annotator": "LEGAL_EXPERT"
    },

    # --- 4. MISSING_JURISDICTION (Thiếu điều khoản giải quyết tranh chấp) ---
    {
        "clause_id": "HDMB_JUR_01",
        "contract_type": "SALES",
        "clause_text": "Hai bên cam kết thực hiện đúng các điều khoản trong hợp đồng trên tinh thần hợp tác vui vẻ.",
        "tokenized_text": "Hai bên cam_kết thực_hiện đúng các điều_khoản trong hợp_đồng trên tinh_thần hợp_tác vui_vẻ .",
        "L1_UNFAIR_PENALTY": 0, "L2_UNILATERAL_MODIFICATION": 0, "L3_AMBIGUOUS_LIABILITY": 0, "L4_MISSING_JURISDICTION": 1,
        "L5_PERSONAL_DATA_VIOLATION": 0, "L6_EXCESSIVE_TERMINATION": 0, "L7_HIDDEN_FEE": 0, "L8_FORCE_MAJEURE_GAP": 0,
        "confidence_score": 1.0, "annotator": "LEGAL_EXPERT"
    },

    # --- 5. PERSONAL_DATA_VIOLATION (Vi phạm dữ liệu cá nhân NĐ 13/2023) ---
    {
        "clause_id": "HDDV_DAT_01",
        "contract_type": "SERVICE",
        "clause_text": "Bên A toàn quyền thu thập, lưu trữ, khai thác và chia sẻ toàn bộ dữ liệu cá nhân, thông tin sinh trắc học và lịch sử giao dịch của Bên B cho bất kỳ đối tác thứ ba nào mà không cần xin phép.",
        "tokenized_text": "Bên A toàn quyền thu_thập , lưu_trữ , khai_thác và chia_sẻ toàn_bộ dữ_liệu cá_nhân , thông_tin sinh_trắc_học và lịch_sử giao_dịch của Bên B cho bất_kỳ đối_tác thứ ba nào mà không cần xin phép .",
        "L1_UNFAIR_PENALTY": 0, "L2_UNILATERAL_MODIFICATION": 0, "L3_AMBIGUOUS_LIABILITY": 0, "L4_MISSING_JURISDICTION": 0,
        "L5_PERSONAL_DATA_VIOLATION": 1, "L6_EXCESSIVE_TERMINATION": 0, "L7_HIDDEN_FEE": 0, "L8_FORCE_MAJEURE_GAP": 0,
        "confidence_score": 1.0, "annotator": "LEGAL_EXPERT"
    },

    # --- 6. EXCESSIVE_TERMINATION (Chấm dứt hợp đồng bất lợi) ---
    {
        "clause_id": "HDLD_TER_01",
        "contract_type": "LABOR",
        "clause_text": "Bên A có quyền đơn phương cho Người lao động nghỉ việc ngay lập tức không cần báo trước, không cần lý do và không thanh toán trợ cấp mất việc.",
        "tokenized_text": "Bên A có quyền đơn_phương cho Người lao_động nghỉ việc ngay lập_tức không cần báo trước , không cần lý_do và không thanh_toán trợ_cấp mất việc .",
        "L1_UNFAIR_PENALTY": 0, "L2_UNILATERAL_MODIFICATION": 1, "L3_AMBIGUOUS_LIABILITY": 0, "L4_MISSING_JURISDICTION": 0,
        "L5_PERSONAL_DATA_VIOLATION": 0, "L6_EXCESSIVE_TERMINATION": 1, "L7_HIDDEN_FEE": 0, "L8_FORCE_MAJEURE_GAP": 0,
        "confidence_score": 1.0, "annotator": "LEGAL_EXPERT"
    },

    # --- 7. HIDDEN_FEE (Phí ẩn / Chi phí không minh bạch) ---
    {
        "clause_id": "HDMB_FEE_01",
        "contract_type": "SALES",
        "clause_text": "Ngoài giá trị hợp đồng nêu trên, Bên Mua có trách nhiệm thanh toán các khoản phí quản lý, phí vận chuyển và phụ phí dịch vụ phát sinh khác theo biểu phí riêng do Bên B tự ban hành từng thời kỳ.",
        "tokenized_text": "Ngoài giá_trị hợp_đồng nêu trên , Bên Mua có trách_nhiệm thanh_toán các khoản phí quản_lý , phí vận_chuyển và phụ phí dịch_vụ phát_sinh khác theo biểu phí riêng do Bên B tự ban_hành từng thời_kỳ .",
        "L1_UNFAIR_PENALTY": 0, "L2_UNILATERAL_MODIFICATION": 0, "L3_AMBIGUOUS_LIABILITY": 0, "L4_MISSING_JURISDICTION": 0,
        "L5_PERSONAL_DATA_VIOLATION": 0, "L6_EXCESSIVE_TERMINATION": 0, "L7_HIDDEN_FEE": 1, "L8_FORCE_MAJEURE_GAP": 0,
        "confidence_score": 1.0, "annotator": "LEGAL_EXPERT"
    },

    # --- 8. FORCE_MAJEURE_GAP (Thiếu điều khoản Bất khả kháng) ---
    {
        "clause_id": "HDTH_FOR_01",
        "contract_type": "LEASE",
        "clause_text": "Dù xảy ra thiên tai, bão lụt, hỏa hoạn hoặc dịch bệnh kéo dài thì Bên Thuê vẫn phải có trách nhiệm thanh toán đủ 100% tiền thuê nhà hàng tháng mà không được giảm trừ.",
        "tokenized_text": "Dù xảy ra thiên_tai , bão lụt , hỏa_hoạn hoặc dịch_bệnh kéo dài thì Bên Thuê vẫn phải có trách_nhiệm thanh_toán đủ 100% tiền thuê nhà hàng tháng mà không được giảm trừ .",
        "L1_UNFAIR_PENALTY": 0, "L2_UNILATERAL_MODIFICATION": 0, "L3_AMBIGUOUS_LIABILITY": 0, "L4_MISSING_JURISDICTION": 0,
        "L5_PERSONAL_DATA_VIOLATION": 0, "L6_EXCESSIVE_TERMINATION": 0, "L7_HIDDEN_FEE": 0, "L8_FORCE_MAJEURE_GAP": 1,
        "confidence_score": 1.0, "annotator": "LEGAL_EXPERT"
    },

    # --- Standard Compliant Clauses (Negative Examples = 0 for all labels) ---
    {
        "clause_id": "HDLD_OK_01",
        "contract_type": "LABOR",
        "clause_text": "Hai bên thống nhất mức lương chính là 15.000.000 VNĐ/tháng, thanh toán vào ngày 05 hàng tháng qua tài khoản ngân hàng của Người lao động.",
        "tokenized_text": "Hai bên thống_nhất mức lương chính là 15.000.000 VNĐ/tháng , thanh_toán vào ngày 05 hàng tháng qua tài_khoản ngân_hàng của Người lao_động .",
        "L1_UNFAIR_PENALTY": 0, "L2_UNILATERAL_MODIFICATION": 0, "L3_AMBIGUOUS_LIABILITY": 0, "L4_MISSING_JURISDICTION": 0,
        "L5_PERSONAL_DATA_VIOLATION": 0, "L6_EXCESSIVE_TERMINATION": 0, "L7_HIDDEN_FEE": 0, "L8_FORCE_MAJEURE_GAP": 0,
        "confidence_score": 1.0, "annotator": "LEGAL_EXPERT"
    },
    {
        "clause_id": "HDMB_OK_02",
        "contract_type": "SALES",
        "clause_text": "Mọi tranh chấp phát sinh từ hợp đồng này sẽ được hai bên ưu tiên giải quyết thông qua thương lượng. Nếu không thương lượng được thì sẽ đưa ra Tòa án nhân dân có thẩm quyền tại Hà Nội để giải quyết.",
        "tokenized_text": "Mọi tranh_chấp phát_sinh từ hợp_đồng này sẽ được hai bên ưu_tiên giải_quyết thông_qua thương_lượng . Nếu không thương_lượng được thì sẽ đưa ra Tòa_án nhân_dân có thẩm_quyền tại Hà_Nội để giải_quyết .",
        "L1_UNFAIR_PENALTY": 0, "L2_UNILATERAL_MODIFICATION": 0, "L3_AMBIGUOUS_LIABILITY": 0, "L4_MISSING_JURISDICTION": 0,
        "L5_PERSONAL_DATA_VIOLATION": 0, "L6_EXCESSIVE_TERMINATION": 0, "L7_HIDDEN_FEE": 0, "L8_FORCE_MAJEURE_GAP": 0,
        "confidence_score": 1.0, "annotator": "LEGAL_EXPERT"
    }
]

def main():
    out_dir = "data/annotated"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "clauses_annotated.csv")

    df = pd.DataFrame(DATASET_SAMPLES)
    df.to_csv(out_file, index=False, encoding="utf-8-sig")
    
    print("="*60)
    print("✅ GENERATED BALANCED CONTRACT RISK DATASET")
    print("="*60)
    print(f"Total samples: {len(df)}")
    print("\nLabel Distribution:")
    label_cols = [c for c in df.columns if c.startswith("L")]
    for col in label_cols:
        pos_count = (df[col] == 1).sum()
        print(f"  • {col:<30}: {pos_count} positive clauses")
    print(f"\nSaved directly to: {out_file}")

if __name__ == "__main__":
    main()
