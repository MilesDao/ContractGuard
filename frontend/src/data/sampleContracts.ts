import { AnalysisResult } from '../types/analysis';

export const SAMPLE_LABOR_CONTRACT: AnalysisResult = {
  contractTitle: 'Hợp đồng Lao động Mẫu (Cảnh báo rủi ro)',
  contractType: 'LABOR',
  overallScore: 78,
  statusGrade: 'RUI_RO_CAO',
  summary: {
    totalClauses: 6,
    riskyClauses: 4,
    criticalCount: 2,
    highCount: 1,
    mediumCount: 1
  },
  analyzedAt: '2026-08-17 15:30',
  clauses: [
    {
      id: 'clause-1',
      clauseNumber: 'Điều 1',
      title: 'Công việc và Địa điểm làm việc',
      text: 'Bên B làm việc ở vị trí Kỹ sư Phần mềm tại trụ sở Bên A. Bên A có quyền toàn quyền điều chuyển Bên B sang bất kỳ chi nhánh hoặc dự án nào trên toàn quốc mà không cần sự đồng ý trước của Bên B.',
      severity: 65,
      labels: ['UNILATERAL_MODIFICATION'],
      explanation: 'Điều khoản cho phép Người sử dụng lao động đơn phương điều chuyển địa điểm làm việc mà không cần sự đồng ý của Người lao động, vi phạm quyền thỏa thuận địa điểm làm việc.',
      legalCitation: 'Bộ luật Lao động 2019 — Điều 29 (Chuyển người lao động làm công việc khác so với hợp đồng lao động phải báo trước ít nhất 03 ngày làm việc).',
      recommendation: 'Sửa đổi: "Bên A chỉ được chuyển Bên B làm việc tại địa điểm khác khi có sự thỏa thuận bằng văn bản của hai bên hoặc theo quy định tại Điều 29 BLLĐ 2019."'
    },
    {
      id: 'clause-2',
      clauseNumber: 'Điều 2',
      title: 'Thời giờ làm việc và Nghỉ ngơi',
      text: 'Thời giờ làm việc là 8 giờ/ngày, từ thứ Hai đến thứ Sáu. Khi có yêu cầu gấp của dự án, Bên B có trách nhiệm tăng ca không giới hạn số giờ và không tính tiền lương tăng ca.',
      severity: 85,
      labels: ['UNFAIR_PENALTY'],
      explanation: 'Yêu cầu làm thêm giờ không giới hạn và không trả lương làm thêm giờ trực tiếp vi phạm quy định về trần giờ làm thêm và nghĩa vụ trả lương tăng ca.',
      legalCitation: 'Bộ luật Lao động 2019 — Điều 107 (Giới hạn giờ làm thêm tối đa 40 giờ/tháng) & Điều 98 (Tiền lương làm thêm giờ ít nhất bằng 150% - 200%).',
      recommendation: 'Sửa đổi: "Làm thêm giờ được thực hiện trên cơ sở tự nguyện, tối đa 40 giờ/tháng và được hưởng tiền lương làm thêm giờ theo Điều 98 BLLĐ 2019."'
    },
    {
      id: 'clause-3',
      clauseNumber: 'Điều 3',
      title: 'Bảo mật Thông tin và Dữ liệu Cá nhân',
      text: 'Bên B đồng ý cho Bên A toàn quyền thu thập, lưu trữ, sử dụng và chia sẻ toàn bộ dữ liệu cá nhân, nhật ký truy cập và thông tin sinh trắc học của Bên B cho bất kỳ đối tác thứ ba nào mà không cần thông báo trước.',
      severity: 95,
      labels: ['PERSONAL_DATA_VIOLATION'],
      explanation: 'Điều khoản vi phạm nghiêm trọng Nghị định 13/2023/NĐ-CP do lấy sự đồng ý tràn lan, không xác định rõ mục đích và chia sẻ dữ liệu sinh trắc học cho bên thứ ba.',
      legalCitation: 'Nghị định 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân — Điều 9 (Quyền của chủ thể dữ liệu) & Điều 11 (Sự đồng ý phải cụ thể, rõ ràng).',
      recommendation: 'Sửa đổi: "Bên A chỉ thu thập và xử lý dữ liệu cá nhân của Bên B phục vụ trực tiếp cho mục đích quản lý lao động. Việc chia sẻ cho bên thứ ba phải có sự đồng ý riêng bằng văn bản của Bên B."'
    },
    {
      id: 'clause-4',
      clauseNumber: 'Điều 4',
      title: 'Phạt vi phạm và Chấm dứt Hợp đồng',
      text: 'Trong trường hợp Bên B nghỉ việc trước thời hạn hợp đồng thì phải bồi thường 200% chi phí đào tạo và chịu phạt 20% tổng thu nhập đã nhận trong suốt thời gian làm việc.',
      severity: 90,
      labels: ['UNFAIR_PENALTY', 'EXCESSIVE_TERMINATION'],
      explanation: 'Mức phạt 20% tổng thu nhập đã nhận và bồi thường 200% chi phí là mức phạt quá đao, bất hợp lý và không đúng quy định pháp luật về phạt vi phạm hợp đồng lao động.',
      legalCitation: 'Bộ luật Dân sự 2015 — Điều 418 (Thỏa thuận phạt vi phạm) & Bộ luật Lao động 2019 (Chi phí đào tạo chỉ hoàn trả phần thực tế chưa sử dụng).',
      recommendation: 'Sửa đổi: "Trường hợp đơn phương chấm dứt hợp đồng trái pháp luật, Người lao động bồi thường chi phí đào tạo thực tế theo quy định tại Điều 62 BLLĐ 2019."'
    },
    {
      id: 'clause-5',
      clauseNumber: 'Điều 5',
      title: 'Giải quyết Tranh chấp',
      text: 'Mọi tranh chấp phát sinh từ hợp đồng này sẽ được giải quyết thông qua thương lượng hòa giải.',
      severity: 40,
      labels: ['MISSING_JURISDICTION'],
      explanation: 'Hợp đồng thiếu quy định về cơ quan tài phán có thẩm quyền (Tòa án nhân dân) khi thương lượng hòa giải không thành công.',
      legalCitation: 'Bộ luật Tố tụng Dân sự 2015 — Điều 35, 39 (Thẩm quyền của Tòa án nhân dân).',
      recommendation: 'Bổ sung: "Nếu không hòa giải được trong vòng 30 ngày, tranh chấp sẽ được đưa ra Tòa án nhân dân có thẩm quyền tại nơi Bên A đặt trụ sở chính để giải quyết."'
    },
    {
      id: 'clause-6',
      clauseNumber: 'Điều 6',
      title: 'Điều khoản Thi hành',
      text: 'Hợp đồng này có hiệu lực kể từ ngày ký, được lập thành 02 bản có giá trị pháp lý như nhau.',
      severity: 0,
      labels: [],
      explanation: 'Điều khoản tiêu chuẩn, phù hợp quy định pháp luật.',
      legalCitation: 'Bộ luật Dân sự 2015 — Điều 401 (Hiệu lực của hợp đồng).',
      recommendation: 'Giữ nguyên.'
    }
  ]
};
