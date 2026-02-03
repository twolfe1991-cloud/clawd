#!/bin/bash
# Test script for agent-browser with Puter.js

echo "========================================="
echo "   Testing Agent Browser + Puter.js"
echo "========================================="
echo ""

# Start agent-browser in background
cd /root/clawd
agent-browser-clawdbot /root/clawd/puter-image-generator.html > /tmp/agent-browser.log 2>&1 &
AGENT_PID=$!

echo "✅ Agent Browser started (PID: $AGENT_PID)"
echo ""
echo "Waiting for agent to launch browser..."
sleep 3

echo ""
echo "========================================="
echo "   Status Check"
echo "========================================="
echo ""

# Check if process is running
if ps -p $AGENT_PID > /dev/null 2>&1; then
    echo "✅ Agent Browser is running"
    echo ""
    echo "📍 Browser should be accessing:"
    echo "   file:///root/clawd/puter-image-generator.html"
    echo ""
    echo "💡 The agent will capture the generated image"
    echo ""
    echo "📋 You can view agent logs:"
    echo "   tail -f /tmp/agent-browser.log"
    echo ""
else
    echo "❌ Agent Browser failed to start"
    echo ""
    echo "📋 Check logs:"
    echo "   cat /tmp/agent-browser.log"
fi

echo ""
echo "========================================="
echo "   To stop agent:"
echo "========================================="
echo ""
echo "   kill $AGENT_PID"
echo ""
echo "========================================="
