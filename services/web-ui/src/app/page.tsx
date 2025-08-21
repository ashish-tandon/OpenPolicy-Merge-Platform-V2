import { api } from '@/lib/api';
import HomePage from '@/components/HomePage';

export default async function Page() {
  // Fetch initial data for the homepage
  const [bills, votes, debates] = await Promise.all([
    api.getBills({ page: 1, privatemember: false }).catch(() => ({ results: [] })),
    api.getBills({ page: 1 }).catch(() => ({ results: [] })), // Using bills as placeholder for votes
    api.getDebates({ page: 1 }).catch(() => ({ results: [] })),
  ]);

  return <HomePage bills={bills} votes={votes} debates={debates} />;
}