from langchain_core.tools import tool
from database import FLIGHTS_DB, HOTELS_DB

# (Dữ liệu FLIGHTS_DB và HOTELS_DB giữ nguyên như bạn đã cung cấp)

def format_currency(amount: int) -> str:
    """Hàm bổ trợ để định dạng tiền tệ: 1000000 -> 1.000.000đ"""
    return f"{amount:,.0f}".replace(",", ".") + "đ"

@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    """
    flights = FLIGHTS_DB.get((origin, destination))
    
    # Nếu không thấy, thử tra ngược lại
    if not flights:
        flights = FLIGHTS_DB.get((destination, origin))
        if flights:
            return f"Không có chuyến trực tiếp từ {origin} đến {destination}. Chỉ có chuyến ngược lại từ {destination} đến {origin}."
        return f"Hiện tại không tìm thấy chuyến bay nào nối giữa {origin} và {destination}."

    result = [f"--- Chuyến bay từ {origin} đến {destination} ---"]
    for f in flights:
        line = (f"- {f['airline']} ({f['class'].capitalize()}): "
                f"{f['departure']} -> {f['arrival']} | Giá: {format_currency(f['price'])}")
        result.append(line)
    
    return "\n".join(result)

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    """
    hotels = HOTELS_DB.get(city)
    if not hotels:
        return f"Xin lỗi, chúng tôi chưa có dữ liệu khách sạn tại {city}."

    # Lọc theo giá và sắp xếp theo rating giảm dần
    filtered_hotels = [h for h in hotels if h['price_per_night'] <= max_price_per_night]
    filtered_hotels.sort(key=lambda x: x['rating'], reverse=True)

    if not filtered_hotels:
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {format_currency(max_price_per_night)}/đêm. Hãy thử tăng ngân sách."

    result = [f"--- Khách sạn tại {city} (Giá dưới {format_currency(max_price_per_night)}) ---"]
    for h in filtered_hotels:
        line = (f"- {h['name']} ({h['stars']}⭐) - Rating: {h['rating']}\n"
                f"  Khu vực: {h['area']} | Giá: {format_currency(h['price_per_night'])}/đêm")
        result.append(line)
    
    return "\n".join(result)

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi định dạng 'tên_khoản:số_tiền,tên_khoản:số_tiền'
    """
    try:
        expense_items = []
        total_expense = 0
        
        # Parse chuỗi expenses
        parts = expenses.split(",")
        for part in parts:
            if ":" not in part:
                continue
            name, price = part.split(":")
            price_val = int(price.strip())
            expense_items.append((name.strip().replace("_", " ").capitalize(), price_val))
            total_expense += price_val
            
        remaining = total_budget - total_expense
        
        # Build bảng chi tiết
        lines = ["Bảng chi phí chi tiết:"]
        for name, price in expense_items:
            lines.append(f"- {name}: {format_currency(price)}")
        
        lines.append("---")
        lines.append(f"Tổng chi: {format_currency(total_expense)}")
        lines.append(f"Ngân sách ban đầu: {format_currency(total_budget)}")
        
        if remaining >= 0:
            lines.append(f"Số dư còn lại: {format_currency(remaining)}")
        else:
            lines.append(f"CẢNH BÁO: Vượt ngân sách {format_currency(abs(remaining))}! Cần điều chỉnh lại kế hoạch.")
            
        return "\n".join(lines)
        
    except Exception as e:
        return "Lỗi định dạng expenses. Vui lòng sử dụng định dạng 'tên:số_tiền,tên:số_tiền' (VD: ve_may_bay:1500000)."