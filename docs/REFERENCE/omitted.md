# Omitted / Deferred Code

List any directories/files not imported, with reason and replacement plan.

## OpenParliament
- `legacy/openparliament/solr/` — deferred; initial search via Postgres FTS
- `legacy/openparliament/static/admin/` — Django admin UI; replace with Next.js admin
- `legacy/openparliament/templates/` — Django templates; replace with React components

## scrapers-ca
- `legacy/scrapers-ca/tests/` — test fixtures may be useful; evaluate after import
- `legacy/scrapers-ca/.github/` — CI configs; adapt to new monorepo structure

## civic-scraper
- `legacy/civic-scraper/examples/` — reference implementations; document patterns
- `legacy/civic-scraper/docs/` — documentation; merge into main docs structure

## Replacement Plans
- **Search**: Postgres FTS → OpenSearch (when scale demands it)
- **Admin UI**: Django admin → Next.js admin with role-based access
- **Templates**: Django templates → React components with shared UI kit
- **CI/CD**: Individual repo configs → unified GitHub Actions workflow
