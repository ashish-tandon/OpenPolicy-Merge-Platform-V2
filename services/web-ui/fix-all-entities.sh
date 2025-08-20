#!/bin/bash

echo "Fixing all HTML entities in TypeScript/TSX files..."

# Fix all HTML entities in one go
find src -name "*.tsx" -print0 | xargs -0 sed -i '' 's/&lsquo;/'"'"'/g'
find src -name "*.tsx" -print0 | xargs -0 sed -i '' 's/&rsquo;/'"'"'/g'
find src -name "*.tsx" -print0 | xargs -0 sed -i '' 's/&quot;/"/g'
find src -name "*.tsx" -print0 | xargs -0 sed -i '' 's/&ldquo;/"/g'
find src -name "*.tsx" -print0 | xargs -0 sed -i '' 's/&rdquo;/"/g'

# Fix the specific problematic patterns
find src -name "*.tsx" -print0 | xargs -0 sed -i '' 's/""rdquo;""rdquo;ldquo;/"/g'
find src -name "*.tsx" -print0 | xargs -0 sed -i '' 's/""rdquo;""rdquo;ldquo;/"/g'

echo "All HTML entities fixed!"
