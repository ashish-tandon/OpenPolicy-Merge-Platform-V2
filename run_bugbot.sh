#!/bin/bash

# Bug Detection Script for Merge V2 Project
# This script runs multiple bug detection tools on your codebase

echo "🐛 Running Bug Detection Tools on Merge V2 Project..."
echo "=================================================="

# Set the project root
PROJECT_ROOT="/Users/ashishtandon/Github/Merge V2"
cd "$PROJECT_ROOT"

# Check if virtual environment exists
if [ ! -d "./services/etl/venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ./services/etl/venv/bin/activate

# Create reports directory
REPORTS_DIR="./bug_reports_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$REPORTS_DIR"
echo "📁 Creating reports in: $REPORTS_DIR"

# 1. Run Bandit (Security Issues)
echo "🔒 Running Bandit security scan..."
bandit -r ./services/ -f json -o "$REPORTS_DIR/bandit_report.json"
echo "✅ Bandit scan completed"

# 2. Run Flake8 (Code Quality)
echo "📝 Running Flake8 code quality check..."
flake8 ./services/ --output-file="$REPORTS_DIR/flake8_report.txt" --max-line-length=120 --ignore=E501,W503
echo "✅ Flake8 check completed"

# 3. Run Safety (Dependency Vulnerabilities)
echo "🛡️ Running Safety dependency check..."
safety check --output json > "$REPORTS_DIR/safety_report.json"
echo "✅ Safety check completed"

# 4. Check Python syntax
echo "🐍 Checking Python syntax..."
find ./services -name "*.py" -exec python3 -m py_compile {} \; 2>&1 | grep -E "(SyntaxError|SyntaxWarning)" > "$REPORTS_DIR/syntax_errors.txt" || echo "No syntax errors found" > "$REPORTS_DIR/syntax_errors.txt"
echo "✅ Syntax check completed"

# 5. Generate summary
echo "📊 Generating summary report..."
{
    echo "# Bug Detection Summary Report"
    echo "Generated on: $(date)"
    echo ""
    echo "## 1. Security Issues (Bandit)"
    echo "Report: $REPORTS_DIR/bandit_report.json"
    echo ""
    echo "## 2. Code Quality Issues (Flake8)"
    echo "Report: $REPORTS_DIR/flake8_report.txt"
    echo ""
    echo "## 3. Dependency Vulnerabilities (Safety)"
    echo "Report: $REPORTS_DIR/safety_report.json"
    echo ""
    echo "## 4. Syntax Errors"
    echo "Report: $REPORTS_DIR/syntax_errors.txt"
    echo ""
    echo "## Quick Stats:"
    echo "- Bandit issues: $(jq '.results | length' "$REPORTS_DIR/bandit_report.json" 2>/dev/null || echo "N/A")"
    echo "- Flake8 issues: $(wc -l < "$REPORTS_DIR/flake8_report.txt" 2>/dev/null || echo "N/A")"
    echo "- Safety issues: $(jq '.vulnerabilities | length' "$REPORTS_DIR/safety_report.json" 2>/dev/null || echo "N/A")"
    echo "- Syntax errors: $(wc -l < "$REPORTS_DIR/syntax_errors.txt" 2>/dev/null || echo "N/A")"
} > "$REPORTS_DIR/SUMMARY.md"

echo "✅ Summary report generated: $REPORTS_DIR/SUMMARY.md"
echo ""
echo "🎯 Bug detection completed! Check the reports in: $REPORTS_DIR"
echo ""
echo "💡 To view results:"
echo "   - Security issues: cat $REPORTS_DIR/bandit_report.json | jq"
echo "   - Code quality: cat $REPORTS_DIR/flake8_report.txt"
echo "   - Dependencies: cat $REPORTS_DIR/safety_report.json | jq"
echo "   - Summary: cat $REPORTS_DIR/SUMMARY.md"
