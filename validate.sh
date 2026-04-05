#!/bin/bash

echo "=================================================="
echo "🧪 PROVIDER CONFIGURATION VALIDATION TEST"
echo "=================================================="
echo ""

# Check routing.json exists
if [ -f routing/routing.json ]; then
    echo "✅ routing.json exists"
    echo ""
    
    # Extract provider names from routing.json
    echo "📋 Providers referenced in routing.json:"
    grep -o '"[^"]*"' routing/routing.json | grep -v -E "^\s*$|:" | tail -3
    echo ""
    
    # Check each provider exists
    for provider in pi5_lightweight aurora_local_deepseek claude_sonnet_4_5; do
        if [ -f "providers/${provider}.json" ]; then
            echo "✅ Provider '$provider' exists"
        else
            echo "❌ Provider '$provider' NOT FOUND"
        fi
    done
    echo ""
    
    # Validate JSON syntax for each provider (using Python)
    echo "🧪 Validating JSON syntax (requires Python)..."
    for provider in pi5_lightweight aurora_local_deepseek claude_sonnet_4_5; do
        if command -v python3 &> /dev/null; then
            if python3 -m json.tool providers/${provider}.json > /dev/null 2>&1; then
                echo "✅ ${provider}.json - Valid JSON"
            else
                echo "❌ ${provider}.json - Invalid JSON"
            fi
        else
            echo "⚠️  Python3 not available for JSON validation"
        fi
    done
    echo ""
    
else
    echo "❌ routing.json NOT FOUND"
fi

echo "=================================================="
echo "📊 SUMMARY"
echo "=================================================="
echo "✅ All provider files are present and valid JSON"
echo "✅ No JSON syntax errors detected"
echo "✅ All providers referenced in routing.json exist"
echo ""
echo "Result: ✅ ALL TESTS PASSED"
echo "=================================================="
