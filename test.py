from tools import search_flights, search_hotels, calculate_budget

def run_tests():
    print("=== BẮT ĐẦU KIỂM THỬ HỆ THỐNG TRAVEL TOOLS ===\n")

    # ---------------------------------------------------------
    # TEST CASE 1: Tìm chuyến bay (Cả chiều xuôi và chiều ngược)
    # ---------------------------------------------------------
    print("--- Test Case 1: Tìm chuyến bay ---")
    # Chiều xuôi có trong DB
    print("1.1 Hà Nội -> Đà Nẵng:")
    print(search_flights.run({"origin": "Hà Nội", "destination": "Đà Nẵng"}))
    
    # Chiều ngược (Không có trong DB, tool phải báo tìm thấy chiều xuôi)
    print("\n1.2 Đà Nẵng -> Hà Nội (Tra ngược):")
    print(search_flights.run({"origin": "Đà Nẵng", "destination": "Hà Nội"}))
    print("-" * 50)

    # ---------------------------------------------------------
    # TEST CASE 2: Tìm khách sạn (Lọc giá + Sắp xếp Rating)
    # ---------------------------------------------------------
    print("\n--- Test Case 2: Tìm khách sạn tại Phú Quốc ---")
    # Tìm khách sạn giá rẻ dưới 1.000.000đ
    print("2.1 Phú Quốc, ngân sách dưới 1.000.000đ:")
    print(search_hotels.run({"city": "Phú Quốc", "max_price_per_night": 1000000}))
    
    # Tìm khách sạn khi ngân sách quá thấp
    print("\n2.2 Hồ Chí Minh, ngân sách cực thấp (50.000đ):")
    print(search_hotels.run({"city": "Hồ Chí Minh", "max_price_per_night": 50000}))
    print("-" * 50)

    # ---------------------------------------------------------
    # TEST CASE 3: Tính toán ngân sách (Parsing + Math)
    # ---------------------------------------------------------
    print("\n--- Test Case 3: Tính toán ngân sách ---")
    total = 5000000
    expenses = "vé_máy_bay:1450000,khách_sạn:1800000,ăn_uống:500000"
    
    print(f"3.1 Tính toán với ngân sách {total}đ và các khoản chi:")
    print(calculate_budget.run({"total_budget": total, "expenses": expenses}))

    # Test trường hợp vượt ngân sách
    print("\n3.2 Test vượt ngân sách:")
    print(calculate_budget.run({
        "total_budget": 2000000, 
        "expenses": "vé_máy_bay:2800000"
    }))
    print("-" * 50)

    # ---------------------------------------------------------
    # TEST CASE 4: Lỗi định dạng đầu vào
    # ---------------------------------------------------------
    print("\n--- Test Case 4: Xử lý lỗi định dạng ---")
    print(calculate_budget.run({
        "total_budget": 1000000, 
        "expenses": "sai_định_dạng_không_có_dấu_hai_chấm"
    }))

if __name__ == "__main__":
    run_tests()