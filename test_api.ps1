# Test script for AI Tutor Backend API
Write-Host "=== Testing AI Tutor Backend API ===" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "1. Testing Health Endpoint..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method GET
    Write-Host "   ✓ Health check passed: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Health check failed: $_" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test 2: Signup (Teacher)
Write-Host "2. Testing Teacher Signup..." -ForegroundColor Yellow
$teacherToken = $null
try {
    $signupBody = @{
        email = "testteacher@example.com"
        password = "testpass123"
        role = "teacher"
    } | ConvertTo-Json
    
    $signupResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/auth/signup" -Method POST -Headers @{"Content-Type"="application/json"} -Body $signupBody
    Write-Host "   ✓ Teacher signup successful!" -ForegroundColor Green
    Write-Host "   Token received: $($signupResponse.access_token.Substring(0, 20))..." -ForegroundColor Gray
    $teacherToken = $signupResponse.access_token
} catch {
    $errorMsg = $_.Exception.Message
    if ($errorMsg -like "*already exists*") {
        Write-Host "   ⚠ User already exists, trying login..." -ForegroundColor Yellow
        try {
            $loginBody = @{
                email = "testteacher@example.com"
                password = "testpass123"
            } | ConvertTo-Json
            $loginResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/auth/login" -Method POST -Headers @{"Content-Type"="application/json"} -Body $loginBody
            $teacherToken = $loginResponse.access_token
            Write-Host "   ✓ Login successful!" -ForegroundColor Green
        } catch {
            Write-Host "   ✗ Login failed: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "   ✗ Signup failed: $_" -ForegroundColor Red
    }
}
Write-Host ""

# Test 3: Signup (Student)
Write-Host "3. Testing Student Signup..." -ForegroundColor Yellow
try {
    $studentBody = @{
        email = "teststudent@example.com"
        password = "testpass123"
        role = "student"
        teacher_id = 1
    } | ConvertTo-Json
    
    $studentResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/auth/signup" -Method POST -Headers @{"Content-Type"="application/json"} -Body $studentBody
    Write-Host "   ✓ Student signup successful!" -ForegroundColor Green
} catch {
    if ($_.Exception.Message -like "*already exists*") {
        Write-Host "   ⚠ Student already exists (this is OK)" -ForegroundColor Yellow
    } else {
        Write-Host "   ✗ Student signup failed: $_" -ForegroundColor Red
    }
}
Write-Host ""

# Test 4: Protected Endpoint (Get Teacher's Students)
Write-Host "4. Testing Protected Endpoint..." -ForegroundColor Yellow
if ($teacherToken) {
    try {
        $headers = @{
            "Authorization" = "Bearer $teacherToken"
            "Content-Type" = "application/json"
        }
        $students = Invoke-RestMethod -Uri "http://127.0.0.1:8000/teachers/me/students" -Method GET -Headers $headers
        Write-Host "   ✓ Protected endpoint works!" -ForegroundColor Green
        Write-Host "   Found $($students.Count) students" -ForegroundColor Gray
    } catch {
        Write-Host "   ✗ Protected endpoint failed: $_" -ForegroundColor Red
    }
} else {
    Write-Host "   ⚠ Skipped (no token available)" -ForegroundColor Yellow
}
Write-Host ""

# Test 5: API Documentation
Write-Host "5. Testing API Documentation..." -ForegroundColor Yellow
try {
    $docs = Invoke-WebRequest -Uri "http://127.0.0.1:8000/docs" -UseBasicParsing
    Write-Host "   ✓ API docs available at http://127.0.0.1:8000/docs" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Docs check failed: $_" -ForegroundColor Red
}
Write-Host ""

Write-Host "=== All Tests Complete ===" -ForegroundColor Cyan
Write-Host "Server is running normally. The continuous loop is expected behavior." -ForegroundColor Green
Write-Host "To stop the server, press Ctrl+C in the terminal where uvicorn is running." -ForegroundColor Yellow
