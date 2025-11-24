# How to Test Your API Endpoints

## ✅ Quick Test Commands

### 1. Health Check
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health"
```

### 2. Teacher Signup
```powershell
$body = '{"email":"newteacher@example.com","password":"pass123","role":"teacher"}'
Invoke-RestMethod -Uri "http://127.0.0.1:8000/auth/signup" -Method POST -Headers @{"Content-Type"="application/json"} -Body $body
```

### 3. Student Signup
```powershell
$body = '{"email":"newstudent@example.com","password":"pass123","role":"student","teacher_id":1}'
Invoke-RestMethod -Uri "http://127.0.0.1:8000/auth/signup" -Method POST -Headers @{"Content-Type"="application/json"} -Body $body
```

### 4. Login
```powershell
$body = '{"email":"newteacher@example.com","password":"pass123"}'
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/auth/login" -Method POST -Headers @{"Content-Type"="application/json"} -Body $body
$token = $response.access_token
```

### 5. Protected Endpoint (Get Students)
```powershell
$headers = @{"Authorization"="Bearer $token"}
Invoke-RestMethod -Uri "http://127.0.0.1:8000/teachers/me/students" -Method GET -Headers $headers
```

### 6. View API Documentation
Open in browser: http://127.0.0.1:8000/docs

## 📝 Notes

- **The server running continuously is NORMAL** - web servers need to stay running to handle requests
- To stop the server: Press `Ctrl+C` in the terminal where uvicorn is running
- All endpoints should return JSON responses
- Check the terminal where uvicorn is running for any error messages

