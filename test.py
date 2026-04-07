import datetime
from agentv2 import graph

def run_agent_test_suite():
    print("="*60)
    print("HỆ THỐNG KIỂM THỬ TỰ ĐỘNG - TRAVEL AGENT AI")
    print("="*60)

    test_scenarios = [
        {
            "id": "Test 1",
            "name": "Direct Answer (Không dùng tool)",
            "user_input": "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.",
            "expectation": "Agent chào hỏi thân thiện, đặt câu hỏi gợi mở về sở thích, ngân sách hoặc thời gian."
        },
        {
            "id": "Test 2",
            "name": "Single Tool Call (Tìm chuyến bay)",
            "user_input": "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng",
            "expectation": "Agent gọi tool search_flights, liệt kê danh sách chuyến bay (thường là 4 chuyến)."
        },
        {
            "id": "Test 3",
            "name": "Multi-Step Tool Chaining (Tư vấn trọn gói)",
            "user_input": "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!",
            "expectation": "Agent gọi liên tiếp: search_flights -> search_hotels -> calculate_budget. Kết quả có bảng tổng hợp chi phí."
        },
        {
            "id": "Test 4",
            "name": "Missing Info (Hỏi lại thông tin thiếu)",
            "user_input": "Tôi muốn đặt khách sạn",
            "expectation": "Agent không gọi tool ngay, yêu cầu người dùng cung cấp: Thành phố, số đêm, hoặc ngân sách."
        },
        {
            "id": "Test 5",
            "name": "Guardrail (Từ chối việc ngoài phạm vi)",
            "user_input": "Giải giúp tôi bài tập lập trình Python về linked list",
            "expectation": "Agent từ chối lịch sự, khẳng định chỉ hỗ trợ các tác vụ liên quan đến du lịch."
        }
    ]

    #Chạy test terminal
    # for test in test_scenarios:
    #     print(f"\n🚀 {test['id']}: {test['name']}")
        
    #     # THỰC THI AGENT
    #     result = graph.invoke({"messages": [("human", test['user_input'])]})
    #     response = result["messages"][-1].content
        
    #     print(f"Agent Response:\n{response}")
    #     print(f"--- [KẾT THÚC {test['id']}] ---")

    # Mở file để ghi kết quả
    with open("test_results.md", "w", encoding="utf-8") as f:
        # Ghi tiêu đề file Markdown
        f.write("# BÁO CÁO KẾT QUẢ KIỂM THỬ AGENT LANGGRAPH\n")
        f.write("**Họ tên: Hoàng Văn Kiên**\n")
        f.write("**MSSV: 2A202600077**\n")
        f.write(f"**Ngày thực hiện:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        f.write("| STT | Kịch bản | Input | Kết quả Agent | Đánh giá |\n")
        f.write("|:---:|:---|:---|:---|:---:|\n")

        print("--- Đang bắt đầu quá trình kiểm thử tự động ---")

        for test in test_scenarios:
            print(f"Đang chạy {test['id']}...")
    
            # Gọi Agent thực tế
            result = graph.invoke({"messages": [("human", test['user_input'])]})
            
            # Lấy câu trả lời cuối cùng
            agent_response = result["messages"][-1].content
            # Xử lý xuống dòng để không làm hỏng bảng Markdown
            formatted_response = agent_response.replace("\n", "<br>").replace("|", "\|")

            # Ghi vào file theo định dạng bảng
            f.write(f"| {test['id']} | {test['name']} | *\"{test['user_input']}\"* | {formatted_response} | [ ] Pass/Fail |\n")

        f.write("\n\n---\n*Ghi chú: Sinh viên tự đánh giá Pass/Fail dựa trên kết quả thực tế và kỳ vọng.*")

    print("\n✅ Hoàn thành! Tất cả kết quả đã được lưu vào file: test_results.md")

if __name__ == "__main__":
    run_agent_test_suite()