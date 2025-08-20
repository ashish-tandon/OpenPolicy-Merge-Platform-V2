#!/bin/bash

echo "Fixing HTML entities in TypeScript/TSX files..."

# Fix HTML entities in TSX files
find src -name "*.tsx" -print0 | xargs -0 sed -i '' 's/&lsquo;/'"'"'/g'
find src -name "*.tsx" -print0 | xargs -0 sed -i '' 's/&rsquo;/'"'"'/g'
find src -name "*.tsx" -print0 | xargs -0 sed -i '' 's/&quot;/"/g'
find src -name "*.tsx" -print0 | xargs -0 sed -i '' 's/&ldquo;/"/g'
find src -name "*.tsx" -print0 | xargs -0 sed -i '' 's/&rdquo;/"/g'

# Fix HTML entities in TS files
find src -name "*.ts" -print0 | xargs -0 sed -i '' 's/&lsquo;/'"'"'/g'
find src -name "*.ts" -print0 | xargs -0 sed -i '' 's/&rsquo;/'"'"'/g'
find src -name "*.ts" -print0 | xargs -0 sed -i '' 's/&quot;/"/g'
find src -name "*.ts" -print0 | xargs -0 sed -i '' 's/&ldquo;/"/g'
find src -name "*.ts" -print0 | xargs -0 sed -i '' 's/&rdquo;/"/g'

echo "HTML entities fixed!"
