#!/bin/bash
# Quick test script for Puter.js Image Generator
# Starts local web server and provides testing instructions

echo "========================================"
echo "   🎨 Puter.js Image Generator"
echo "========================================"
echo ""
echo "Starting local web server..."
echo ""

# Start server in background
cd /root/clawd
python3 -m http.server 8080 > /tmp/puter-server.log 2>&1 &
SERVER_PID=$!

echo "✅ Server started (PID: $SERVER_PID)"
echo ""
echo "📍 Open this URL in your browser:"
echo ""
echo "   http://localhost:8080/puter-image-generator.html"
echo ""
echo "========================================"
echo "   Testing Instructions"
echo "========================================"
echo ""
echo "1. Select model: 'gemini-25-flash' (Nano Banana)"
echo "2. Enter prompt: 'A cute cat in a spacesuit'"
echo "3. Click 'Generate Image'"
echo "4. Wait for image to appear"
echo ""
echo "✅ Success = Image appears below button!"
echo "❌ Error = Status message appears"
echo ""
echo "========================================"
echo "   To stop server:"
echo "========================================"
echo ""
echo "   kill $SERVER_PID"
echo ""
echo "========================================"

# Wait for user
read -p "Press Enter to stop server..."

# Cleanup
kill $SERVER_PID 2>/dev/null
echo ""
echo "✅ Server stopped"
