import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000"

print("=" * 60)
print("AI TUTOR - SYSTEM HEALTH CHECK")
print("=" * 60)

# Test endpoints
endpoints = [
    ("GET", "/health", None),
    ("GET", "/api/chat/history?user_id=student_demo", None),
    ("GET", "/api/homework/history?user_id=student_demo", None),
    ("GET", "/api/exam/history?user_id=student_demo", None),
    ("GET", "/api/learning/recommendations/student_demo", None),
]

results = []

for method, path, data in endpoints:
    url = f"{BASE_URL}{path}"
    print(f"\n[{method}] {path}")
    
    try:
        if method == "GET":
            with urllib.request.urlopen(url, timeout=5) as response:
                status = response.status
                if status == 200:
                    print(f"  ✅ Status: {status} OK")
                    results.append((path, "✅ PASS"))
                else:
                    print(f"  ⚠️  Status: {status}")
                    results.append((path, f"⚠️  {status}"))
        else:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method=method
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                status = response.status
                if status == 200:
                    print(f"  ✅ Status: {status} OK")
                    results.append((path, "✅ PASS"))
                else:
                    print(f"  ⚠️  Status: {status}")
                    results.append((path, f"⚠️  {status}"))
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        results.append((path, f"❌ FAIL"))

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

passed = sum(1 for _, status in results if "✅" in status)
total = len(results)

for path, status in results:
    print(f"{status} {path}")

print(f"\nTotal: {passed}/{total} endpoints passed")

if passed == total:
    print("\n🎉 ALL SYSTEMS OPERATIONAL!")
else:
    print(f"\n⚠️  {total - passed} endpoint(s) need attention")
