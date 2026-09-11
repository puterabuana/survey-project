#!/bin/bash

# Quick Test Script for Survey Platform

echo "🧪 Testing Survey Platform..."
echo ""

# Check if server is running
if pgrep -f "python3 app.py" > /dev/null; then
    echo "✅ Server is running"
else
    echo "⚠️ Server not running. Starting..."
    cd ~/survey-project
    python3 app.py &
    sleep 3
fi

echo ""
echo "Testing endpoints..."
echo ""

# Test homepage
echo "1. Testing homepage (/)..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000)
if [ "$STATUS" -eq 200 ]; then
    echo "   ✅ Homepage OK (Status: $STATUS)"
else
    echo "   ❌ Homepage failed (Status: $STATUS)"
fi

# Test admin
echo "2. Testing admin dashboard (/admin)..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/admin)
if [ "$STATUS" -eq 200 ]; then
    echo "   ✅ Admin dashboard OK (Status: $STATUS)"
else
    echo "   ❌ Admin dashboard failed (Status: $STATUS)"
fi

# Test API stats
echo "3. Testing stats API (/api/stats)..."
RESPONSE=$(curl -s http://localhost:5000/api/stats)
if [[ $RESPONSE == *"total_logins"* ]]; then
    echo "   ✅ API working"
    echo "   Stats: $RESPONSE"
else
    echo "   ❌ API failed"
fi

echo ""
echo "📊 Test Summary:"
echo "   Main page: http://localhost:5000"
echo "   Admin: http://localhost:5000/admin"
echo "   API: http://localhost:5000/api/stats"
echo ""
echo "Next steps:"
echo "1. Open browser and test login with test.user@binus.ac.id"
echo "2. Fill survey form"
echo "3. Check admin dashboard"
echo "4. Deploy to Railway/Render when ready"
