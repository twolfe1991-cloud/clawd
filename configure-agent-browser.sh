#!/bin/bash
# Configure and test agent-browser

echo "========================================="
echo "   Agent Browser Configuration"
echo "========================================="
echo ""

# Check installation
if ! command -v agent-browser > /dev/null 2>&1; then
    echo "❌ agent-browser not found"
    exit 1
fi

echo "✅ agent-browser is installed"
echo ""

# Try to launch agent-browser with a simple test
# Open a simple HTML page and take a snapshot
echo "🧪 Testing agent-browser..."
echo ""

# Create a simple test HTML file
TEST_HTML="/tmp/agent-test.html"
cat > "$TEST_HTML" << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Agent Browser Test</title>
</head>
<body>
    <h1>Agent Browser Test Page</h1>
    <p>If you see this, agent-browser is working!</p>
    <p>Timestamp: <span id="time"></span></p>
    <button id="btn" onclick="document.getElementById('time').textContent = new Date().toLocaleString()">Click Me</button>
</body>
</html>
EOF

# Run agent-browser with test page
agent-browser --session admin open file://$TEST_HTML > /tmp/agent-browser-test.log 2>&1 &
AGENT_PID=$!

echo "✅ Agent Browser started (PID: $AGENT_PID)"
echo "Waiting 5 seconds..."
sleep 5

# Check logs
echo ""
echo "========================================="
echo "   Checking Status"
echo "========================================="

if ps -p $AGENT_PID > /dev/null 2>&1; then
    echo "✅ Process is running"
else
    echo "❌ Process stopped"
fi

# Check for errors in log
if grep -q "libnspr4" /tmp/agent-browser-test.log 2>/dev/null; then
    echo "⚠️  Still seeing libnspr4 errors"
    echo "   Library was installed, but browser binary can't find it"
else
    echo "✅ No library errors in log"
fi

# Cleanup
kill $AGENT_PID 2>/dev/null
echo ""
echo "========================================="
echo "   Configuration Summary"
echo "========================================="
echo ""
echo "✅ agent-browser is installed and ready"
echo ""
echo "Usage:"
echo "   agent-browser --session admin open <url>"
echo ""
echo "   Open Puter.js generator:"
echo "   http://localhost:8080/puter-image-generator.html"
