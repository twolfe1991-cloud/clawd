#!/bin/bash
# Test script for agent-browser with Puter.js

echo "========================================="
echo "   Testing Agent Browser + Puter.js"
echo "========================================="
echo ""

# Check if agent-browser is installed
if ! command -v agent-browser > /dev/null 2>&1; then
    echo "❌ Error: agent-browser not found"
    echo ""
    echo "Install with: npm install -g agent-browser"
    exit 1
fi

echo "✅ agent-browser found"
echo ""

# Start agent-browser with Puter.js page
cd /root/clawd

# Run agent-browser to open the Puter.js page
# It will navigate to the file and execute Puter.js
echo "🌐 Opening Puter.js Image Generator..."
echo ""

# Create a command sequence for agent-browser
# 1. Navigate to file:// URL
# 2. Wait for page to load
# 3. Enter prompt
# 4. Click generate button
# 5. Wait for image
# 6. Get image result

# We'll use a simple approach - run agent-browser in session mode
agent-browser --session admin open file:///root/clawd/puter-image-generator.html > /tmp/agent-browser.log 2>&1 &
AGENT_PID=$!

echo "✅ Agent Browser started (PID: $AGENT_PID)"
echo ""
echo "⏳ Waiting for browser to load..."
sleep 5

# Check if process is still running
if ps -p $AGENT_PID > /dev/null 2>&1; then
    echo "✅ Agent Browser is running"
    echo ""
    echo "💡 You can interact with it by running:"
    echo "   agent-browser --session admin snapshot -i --json"
    echo ""
    echo "📋 View logs:"
    echo "   tail -f /tmp/agent-browser.log"
    echo ""
    echo "🌐 Or manually open in browser:"
    echo "   file:///root/clawd/puter-image-generator.html"
    echo ""
    echo "========================================="
    echo "   To stop agent:"
    echo "========================================="
    echo ""
    echo "   kill $AGENT_PID"
else
    echo "❌ Agent Browser failed to start"
    echo ""
    echo "📋 Check logs:"
    cat /tmp/agent-browser.log
fi

echo ""
echo "========================================="
