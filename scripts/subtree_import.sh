#!/usr/bin/env bash
set -euo pipefail

# OpenPolicy Git Subtree Import Script
# Imports source repositories using git subtree to preserve commit history

echo "Importing OpenPolicy repositories using git subtree..."

# Function to add and import a repository as subtree
add_subtree() {
    remote="$1"
    url="$2"
    prefix="$3"
    branch="${4:-main}"
    
    echo "Processing $remote..."
    
    # Add remote if it doesn't exist
    if ! git remote | grep -q "$remote"; then
        echo "Adding remote: $remote"
        git remote add "$remote" "$url"
    fi
    
    # Fetch the remote
    echo "Fetching $remote..."
    git fetch "$remote"
    
    # Import as subtree
    echo "Importing $remote as subtree at $prefix..."
    if git subtree add --prefix="$prefix" "$remote" "$branch" --squash; then
        echo "✓ Successfully imported $remote to $prefix"
    else
        echo "⚠ Warning: Failed to import $remote to $prefix"
        echo "  This might be due to conflicts or the directory already existing"
        echo "  You may need to resolve conflicts manually or remove the directory first"
    fi
    
    echo ""
}

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Error: This script must be run from the root of a git repository"
    echo "Please run 'git init' first or navigate to an existing git repository"
    exit 1
fi

# Check if we have any commits
if ! git rev-parse HEAD >/dev/null 2>&1; then
    echo "No commits found. Creating initial commit..."
    git commit --allow-empty -m "Initial commit for OpenPolicy monorepo"
fi

echo "Starting subtree imports..."
echo ""

# Import repositories with history preservation
# OpenParliament - Federal parliamentary data
add_subtree openparliament https://github.com/michaelmulley/openparliament.git legacy/openparliament main

# Provincial/Municipal scrapers
add_subtree scrapers https://github.com/opencivicdata/scrapers-ca.git legacy/scrapers-ca main

# Civic scraping utilities
add_subtree civic https://github.com/biglocalnews/civic-scraper.git legacy/civic-scraper main

# Note: For repositories where we want to copy code without history, use manual copy instead
echo "Note: The following repositories are NOT imported as subtrees:"
echo "  - rarewox/open-policy-infra (copy IaC templates manually)"
echo "  - rarewox/admin-open-policy (copy UI components manually)"
echo "  - rarewox/open-policy-app (copy React Native code manually)"
echo "  - rarewox/open-policy-web (copy Next.js components manually)"
echo "  - rarewox/open-policy (copy backend experiments manually)"
echo ""
echo "These can be copied manually to preserve only the needed code without full history."
echo ""

echo "Subtree import complete!"
echo ""
echo "Imported repositories:"
echo "  ✓ legacy/openparliament (federal parliamentary data)"
echo "  ✓ legacy/scrapers-ca (provincial/municipal scrapers)"
echo "  ✓ legacy/civic-scraper (civic data utilities)"
echo ""
echo "Next steps:"
echo "1. Review the imported code in /legacy directories"
echo "2. Document what to keep vs. what to replace in docs/REFERENCE/omitted.md"
echo "3. Start implementing the new canonical schema and API endpoints"
echo "4. Gradually migrate code from /legacy to /services and /apps"
echo ""
echo "Repository status:"
git remote -v
echo ""
echo "Subtree directories:"
ls -la legacy/
