
import os

def print_errors(text):
    for line in text.splitlines():
        if "FAIL" in line or "Error" in line or "Traceback" in line or "ImportError" in line:
            print(line)

try:
    with open("debug_output_2.txt", "r", encoding="utf-16") as f:
        print(f.read())
except Exception:
    try:
        with open("debug_output_2.txt", "r", encoding="utf-8") as f:
            print(f.read())
    except Exception as e:
        print(f"Failed to read file: {e}")
