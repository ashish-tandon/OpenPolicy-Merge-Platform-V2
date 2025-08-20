# OpenParliament.ca Web UI Implementation

A modern Next.js implementation of OpenParliament.ca features, providing access to Canadian parliamentary data.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Set up environment variables
cp .env.local.example .env.local

# Run development server
npm run dev

# Open http://localhost:3000
```

## 📊 Implementation Status

- **84/120+ features implemented** (70% complete)
- **All UI components built** with TypeScript and Tailwind CSS
- **Connected to FastAPI backend** at http://localhost:8000

See [FINAL_IMPLEMENTATION_STATUS.md](./FINAL_IMPLEMENTATION_STATUS.md) for detailed feature list.

## 🏗️ Architecture

```
src/
├── app/                    # Next.js App Router pages
│   ├── bills/             # Bills & legislation
│   ├── committees/        # Parliamentary committees
│   ├── debates/           # Hansard transcripts
│   ├── labs/             # Experimental features
│   ├── mps/              # MP profiles
│   └── search/           # Search functionality
├── components/            # Reusable React components
│   ├── Bills/            # Bill-specific components
│   ├── Committees/       # Committee components
│   ├── Debates/          # Debate/Hansard components
│   ├── MPs/              # MP-related components
│   └── Search/           # Search components
├── lib/                   # Utilities and API client
└── legacy-migration/      # Legacy OpenParliament code
```

## 🎯 Features Implemented

### Homepage & Navigation (13 features)
- Global search with autocomplete
- Real-time House status
- Dynamic word clouds
- Recent bills/votes tracking
- Responsive navigation

### MP Management (19 features)
- Complete MP profiles
- Voting records
- Speech archive
- Committee membership
- Electoral history

### Bills & Legislation (21 features)
- Bill status tracking
- Amendment tracking
- Vote outcomes
- Committee review
- Related debates

### Debates & Hansard (12 features)
- 30+ year archive
- AI summaries (mocked)
- Topic extraction
- Speaker attribution
- Cross-reference linking

### Committee System (10 features)
- Committee profiles
- Member tracking
- Active studies
- Meeting schedules
- Report management

### Labs Features (9 features)
- Parliamentary Haiku generator
- Poetry extraction
- Data visualizations
- Experimental features

## 🔧 Development

```bash
# Type checking
npm run type-check

# Linting
npm run lint

# Build for production
npm run build

# Start production server
npm start
```

## 🌐 API Integration

The UI connects to the FastAPI backend. Ensure the backend is running:

```bash
cd ../../
make api  # Starts the FastAPI server on port 8000
```

## 📱 Responsive Design

- Mobile-first approach
- Touch-optimized interfaces
- Adaptive layouts
- Progressive enhancement

## 🎨 UI Components

All components follow a consistent design system:
- TypeScript for type safety
- Tailwind CSS for styling
- Accessibility best practices
- Loading and error states

## 🧪 Testing Features

1. **Homepage**: Check word cloud, recent bills, house status
2. **Search**: Try postal codes (e.g., M5V3A8), MP names, bill numbers
3. **MPs**: Browse by province/party, view profiles
4. **Bills**: Filter by type/session, track status
5. **Debates**: Browse Hansard, view AI summaries
6. **Committees**: Explore committees, members, studies
7. **Labs**: Try Haiku generator and poetry finder

## 🐛 Known Issues

- Votes API disabled (recursion error in backend)
- AI features use mock data
- No real-time updates (WebSocket not implemented)
- Authentication system not connected
- Some data is mocked where APIs are missing

## 📚 Resources

- [OpenParliament.ca](https://openparliament.ca)
- [Feature Inventory](../docs/Open Parliament Migration Plan/02-feature-inventory.md)
- [Migration Plan](../docs/Open Parliament Migration Plan/README.md)
- [API Documentation](../openapi.yaml)

## 🤝 Contributing

This is part of the OpenPolicy Merge Platform V2. See the main repository documentation for contribution guidelines.

## 📄 License

<<<<<<< Current (Your changes)
Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
=======
Same as the parent OpenPolicy project.
>>>>>>> Incoming (Background Agent changes)
