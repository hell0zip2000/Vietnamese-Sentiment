from vietnamese_utils import preprocess_text
import sys
import os

# Thêm một số màu sắc cho output
GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

def run_test(test_name, input_text, expected_output=None, expected_error=None):
    print(f"\n--- Bắt đầu Test: {test_name} ---")
    print(f"Input gốc: '{input_text}'")
    
    try: 
        actual_output = preprocess_text(input_text)
        
        if expected_error:
            print(f"{RED}THẤT BẠI:{ENDC} Đáng lẽ phải có lỗi '{expected_error}', nhưng lại thành công.")
            return False
        
        if actual_output == expected_output:
            print(f"{GREEN}THÀNH CÔNG:{ENDC} Output chuẩn hóa: '{actual_output}'")
            return True
        else: 
            print(f"{RED}THẤT BẠI:{ENDC} Output thực tế: '{actual_output}' | Output mong đợi: '{expected_output}'")
            return False 
        
    except ValueError as e:
        if expected_error == "ValueError": 
            print(f"{GREEN}THÀNH CÔNG:{ENDC} Bắt được lỗi: {e}")
            return True
        else: 
            print(f"{RED}THẤT BẠI:{ENDC} Bắt được lỗi không mong đợi: {e}")
            return False
        
    except Exception as e:
        print(f"{RED}THẤT BẠI:{ENDC} Lỗi không xác định: {e}")
        return False
    
    return False 

if __name__ == "__main__": 
    results = [] 
    
    r1 = run_test(
        "Viết tắt đơn giản",
        "cai mon nay an ko ngon lam",
        expected_output="Cái món này ăn không ngon lắm"
    )
    results.append(r1) 
    
    r2 = run_test(
        "Lỗi nhập liệu", 
        "ok", 
        expected_error="ValueError"
    )
    results.append(r2) 
    
    r3 = run_test(
        "Chuẩn hóa kết hợp", 
        "Cái này Bt lun", 
        expected_output="cái này bình thường luôn" 
    )
    results.append(r3)
    
    r4 = run_test(
        "Tách từ (Vietnamese)", 
        "đất nước tôi rất đẹp",
        expected_output="đất_nước tôi rất đẹp" 
    )
    results.append(r4)
    
    # --- Tổng kết ---
    success_count = sum(results)
    total_count = len(results)
    print(f"\n======================================")
    print(f"TỔNG KẾT: {success_count}/{total_count} bài kiểm tra thành công.")
    print(f"======================================")