import os
import json

def check_files():
    required = ["audit_log.jsonl", "orders_clean.csv", "pharmeasy.db"]
    missing = [f for f in required if not os.path.exists(f)]
    
    if missing:
        print(f"FAIL: Missing files {missing}")
        return False
    
    if os.path.getsize("audit_log.jsonl") == 0:
        print("FAIL: audit_log empty")
        return False
        
    print("PASS: All review gates passed")
    return True

if __name__ == "__main__":
    ok = check_files()
    exit(0 if ok else 1)
