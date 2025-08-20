#!/usr/bin/env bash
set -euo pipefail

# OpenPolicy Repository Cloning Script
# Clones all source repositories to /legacy directory for reference and analysis

echo "Setting up OpenPolicy legacy code reference structure..."

# Create legacy directory structure
mkdir -p legacy/{openparliament,scrapers-ca,civic-scraper,open-policy-infra,admin-open-policy,open-policy-app,open-policy-web,open-policy}

# Function to clone repository and copy to legacy
clone_to_legacy() {
    repo="$1"
    legacy_dir="$2"

    echo "Processing $legacy_dir..."

    # Create temporary clone directory
    temp_dir=$(mktemp -d)

    if git clone "$repo" "$temp_dir" 2>/dev/null; then
        echo "✓ Cloned $repo"

        # Copy contents to legacy directory
        cp -r "$temp_dir"/* "$legacy_dir/" 2>/dev/null || true
        cp -r "$temp_dir"/.* "$legacy_dir/" 2>/dev/null || true

        # Remove .git directory (we don't need history in legacy)
        rm -rf "$legacy_dir/.git" 2>/dev/null || true

        echo "✓ Copied to legacy/$legacy_dir"

        # Show size
        size=$(du -sh "$legacy_dir" | cut -f1)
        echo "  Size: $size"
    else
        echo "⚠ Failed to clone $repo"
    fi

    # Cleanup temp directory
    rm -rf "$temp_dir"
    echo ""
}

echo "Cloning repositories to legacy directory..."
echo ""

# Clone all source repositories to legacy
clone_to_legacy "https://github.com/michaelmulley/openparliament.git" "openparliament"
clone_to_legacy "https://github.com/rarewox/open-policy-infra.git" "open-policy-infra"
clone_to_legacy "https://github.com/rarewox/admin-open-policy.git" "admin-open-policy"
clone_to_legacy "https://github.com/rarewox/open-policy-app.git" "open-policy-app"
clone_to_legacy "https://github.com/rarewox/open-policy-web.git" "open-policy-web"
clone_to_legacy "https://github.com/rarewox/open-policy.git" "open-policy"
clone_to_legacy "https://github.com/opencivicdata/scrapers-ca.git" "scrapers-ca"
clone_to_legacy "https://github.com/biglocalnews/civic-scraper.git" "civic-scraper"

echo ""
echo "Legacy code setup complete!"
echo ""
echo "Legacy directory structure:"
ls -la legacy/
echo ""
echo "Repository sizes:"
du -sh legacy/* | sort -hr
echo ""
echo "Next steps:"
echo "1. Review legacy code to understand each codebase"
echo "2. Focus on OpenParliament first (legacy/openparliament/)"
echo "3. Document key components in docs/REFERENCE/omitted.md"
echo "4. Start implementing the new canonical schema"
echo ""
echo "Note: Legacy code is gitignored and won't be committed"
echo "This is for reference only during the migration process"
