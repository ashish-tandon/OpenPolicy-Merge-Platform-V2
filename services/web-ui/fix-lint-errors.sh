#!/bin/bash

# Fix unescaped entities in about page
echo "Fixing /src/app/about/page.tsx..."
sed -i "s/We'd love to hear from you/We\&apos;d love to hear from you/g" src/app/about/page.tsx

# Fix unescaped entities in labs/haiku/page.tsx
echo "Fixing /src/app/labs/haiku/page.tsx..."
sed -i 's/"{haiku.source.originalText}"/\&quot;{haiku.source.originalText}\&quot;/g' src/app/labs/haiku/page.tsx

# Fix unescaped entities in labs/page.tsx
echo "Fixing /src/app/labs/page.tsx..."
sed -i "s/We're experimenting/We\&apos;re experimenting/g" src/app/labs/page.tsx
sed -i "s/don't make it/don\&apos;t make it/g" src/app/labs/page.tsx

# Fix unescaped entities in represent pages
echo "Fixing /src/app/represent/api/page.tsx..."
sed -i "s/'representatives'\/'/\&apos;representatives\&apos;\/\&apos;/g" src/app/represent/api/page.tsx
sed -i "s/'boundaries'/\&apos;boundaries\&apos;/g" src/app/represent/api/page.tsx
sed -i "s/'elections'/\&apos;elections\&apos;/g" src/app/represent/api/page.tsx
sed -i "s/'candidates'/\&apos;candidates\&apos;/g" src/app/represent/api/page.tsx

echo "Fixing /src/app/represent/demo/page.tsx..."
sed -i 's/"postal-code"/\&quot;postal-code\&quot;/g' src/app/represent/demo/page.tsx

echo "Fixing /src/app/represent/page.tsx..."
sed -i "s/Canada's open/Canada\&apos;s open/g" src/app/represent/page.tsx
sed -i 's/"representatives"/\&quot;representatives\&quot;/g' src/app/represent/page.tsx
sed -i "s/who's who/who\&apos;s who/g" src/app/represent/page.tsx
sed -i "s/It's a/It\&apos;s a/g" src/app/represent/page.tsx

echo "Fixing /src/app/search/page.tsx..."
sed -i 's/"climate change"/\&quot;climate change\&quot;/g' src/app/search/page.tsx

# Fix unescaped entities in components
echo "Fixing /src/components/Bills/BillAnalysis.tsx..."
sed -i "s/bill's impact/bill\&apos;s impact/g" src/components/Bills/BillAnalysis.tsx
sed -i "s/won't significantly/won\&apos;t significantly/g" src/components/Bills/BillAnalysis.tsx

echo "Fixing /src/components/Bills/RelatedDebates.tsx..."
sed -i 's/"climate change"/\&quot;climate change\&quot;/g' src/components/Bills/RelatedDebates.tsx

echo "Fixing /src/components/Debates/DebatesFilters.tsx..."
sed -i "s/MP's name/MP\&apos;s name/g" src/components/Debates/DebatesFilters.tsx

echo "Fixing /src/components/SearchBar.tsx..."
sed -i 's/"climate change"/\&quot;climate change\&quot;/g' src/components/SearchBar.tsx

echo "All unescaped entities fixed!"