import Link from 'next/link';

interface Vote {
  id: number;
  number: number;
  session: string;
  description: string;
  result: 'Passed' | 'Failed' | 'Tied';
  date: string;
  yea_total: number;
  nay_total: number;
}

interface RecentVotesProps {
  votes: any[]; // Using any temporarily until votes API is fixed
}

export default function RecentVotes({ votes }: RecentVotesProps) {
  // Placeholder data until votes API is fixed
  const placeholderVotes: Vote[] = [
    {
      id: 1,
      number: 123,
      session: '45-1',
      description: 'Motion for second reading of Bill C-5',
      result: 'Passed',
      date: '2025-06-20',
      yea_total: 178,
      nay_total: 145,
    },
    {
      id: 2,
      number: 122,
      session: '45-1',
      description: 'Amendment to Bill C-3',
      result: 'Failed',
      date: '2025-06-19',
      yea_total: 145,
      nay_total: 178,
    },
    {
      id: 3,
      number: 121,
      session: '45-1',
      description: 'Motion for third reading of Bill C-2',
      result: 'Passed',
      date: '2025-06-18',
      yea_total: 200,
      nay_total: 123,
    },
  ];

  const displayVotes = votes.length > 0 ? votes : placeholderVotes;

  return (
    <ul className="space-y-3">
      {displayVotes.slice(0, 5).map((vote) => (
        <li key={vote.id}>
          <Link 
            href={`/votes/${vote.session}/${vote.number}`}
            className="block hover:bg-gray-50 -mx-2 px-2 py-1 rounded"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-medium text-op-blue hover:underline">
                Vote #{vote.number}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded font-medium ${
                vote.result === 'Passed' 
                  ? 'bg-green-100 text-green-800' 
                  : vote.result === 'Failed'
                  ? 'bg-red-100 text-red-800'
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {vote.result}
              </span>
            </div>
            <div className="text-sm text-gray-600 line-clamp-2">
              {vote.description}
            </div>
            <div className="text-xs text-gray-500 mt-1">
              {vote.yea_total} yea, {vote.nay_total} nay
            </div>
          </Link>
        </li>
      ))}
    </ul>
  );
}
