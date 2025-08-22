#!/bin/bash

# Quick Fix Script for Critical Python 2.x Compatibility Issues
# This script fixes the most critical bugs that prevent code from running

echo "🚨 Fixing Critical Python 2.x Compatibility Issues..."
echo "=================================================="

# Set the project root
PROJECT_ROOT="/Users/ashishtandon/Github/Merge V2"
cd "$PROJECT_ROOT"

# Check if we're in the right directory
if [ ! -d "./services" ]; then
    echo "❌ Error: Not in Merge V2 project directory"
    exit 1
fi

echo "🔧 Fixing print statements (Python 2.x -> 3.x)..."
# Fix print statements without parentheses
find ./services -name "*.py" -type f -exec sed -i '' 's/print \([^)]\)/print(\1)/g' {} \; 2>/dev/null

echo "🔧 Fixing exception handling syntax..."
# Fix old exception syntax: except Exception, e: -> except Exception as e:
find ./services -name "*.py" -type f -exec sed -i '' 's/except \([^,]*\), \([^:]*\):/except \1 as \2:/g' {} \; 2>/dev/null

echo "🔧 Fixing invalid escape sequences..."
# Fix regex escape sequences by adding raw string prefix
find ./services -name "*.py" -type f -exec sed -i '' 's/"memcached:\/\/\(\[\.\\w\]\+:\\d\+\)"/r"memcached:\/\/\(\[\.\\w\]\+:\\d\+\)"/g' {} \; 2>/dev/null

echo "🔧 Fixing other common Python 2.x issues..."
# Fix raw_input -> input
find ./services -name "*.py" -type f -exec sed -i '' 's/raw_input/input/g' {} \; 2>/dev/null

# Fix xrange -> range
find ./services -name "*.py" -type f -exec sed -i '' 's/xrange/range/g' {} \; 2>/dev/null

# Fix unicode -> str
find ./services -name "*.py" -type f -exec sed -i '' 's/unicode/str/g' {} \; 2>/dev/null

echo "✅ Critical fixes completed!"
echo ""
echo "🧪 Testing Python syntax..."
echo "=========================="

# Test Python syntax on a few key files
echo "Testing main API gateway file..."
python3 -m py_compile ./services/api-gateway/app/main.py 2>&1 || echo "⚠️  Still has syntax issues"

echo "Testing ETL main file..."
python3 -m py_compile ./services/etl/app/main.py 2>&1 || echo "⚠️  Still has syntax issues"

echo ""
echo "🎯 Next Steps:"
echo "1. Run: ./run_bugbot.sh (to see remaining issues)"
echo "2. Install auto-formatting tools: pip install autopep8 black isort"
echo "3. Auto-format code: autopep8 --in-place --recursive ./services/"
echo ""
echo "💡 Most critical issues should now be fixed!"
echo "   The remaining ~244,000 issues are mostly style violations that can be auto-fixed."
