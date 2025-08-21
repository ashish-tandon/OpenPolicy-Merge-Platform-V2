'use client';

import Link from 'next/link';
import { useTranslation } from '@/hooks/useTranslation';
import HouseStatus from '@/components/HouseStatus';
import WordCloud from '@/components/WordCloud';
import RecentBills from '@/components/RecentBills';
import RecentVotes from '@/components/RecentVotes';
import FeaturedDebate from '@/components/FeaturedDebate';
import AnimatedBackground from '@/components/AnimatedBackground';
import { ArrowRightIcon } from '@heroicons/react/24/outline';

interface HomePageProps {
  bills: any;
  votes: any;
  debates: any;
}

export default function HomePage({ bills, votes, debates }: HomePageProps) {
  const { t } = useTranslation();

  return (
    <>
      <AnimatedBackground />
      <div className="content-container py-8">
      {/* House Status Banner */}
      <HouseStatus />

      {/* Hero Section */}
      <div className="text-center py-16 animate-fade-in">
        <h1 className="text-5xl md:text-6xl font-bold mb-6 text-gradient">
          {t('home.hero.title')}
        </h1>
        <p className="text-xl text-muted-foreground mb-8 max-w-3xl mx-auto">
          {t('home.hero.subtitle')}
        </p>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column - Featured Content */}
        <div className="lg:col-span-2 space-y-8">
          {/* Word Cloud */}
          <div className="card-hover p-6 animate-fade-in-up">
            <h2 className="text-2xl font-bold mb-4">
              {t('home.wordCloud.title')}
            </h2>
            <p className="text-sm text-muted-foreground mb-4">
              {t('home.wordCloud.subtitle')}
            </p>
            <WordCloud />
          </div>

          {/* Featured Debate */}
          <div className="card-hover p-6 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
            <h2 className="text-2xl font-bold mb-4">
              Latest House Transcript
            </h2>
            <FeaturedDebate debates={debates} />
          </div>
        </div>

        {/* Right Column - Recent Activity */}
        <div className="space-y-8">
          {/* Recent Bills */}
          <div className="card-hover p-6 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold">{t('home.recentBills.title')}</h3>
              <Link href="/bills" className="text-primary hover:text-primary/80 transition-colors">
                {t('home.recentBills.viewAll')}
              </Link>
            </div>
            <RecentBills bills={bills} />
          </div>

          {/* Recent Votes */}
          <div className="card-hover p-6 animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold">{t('home.recentVotes.title')}</h3>
              <Link href="/votes" className="text-primary hover:text-primary/80 transition-colors">
                {t('home.recentVotes.viewAll')}
              </Link>
            </div>
            <RecentVotes votes={votes} />
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="mt-16">
        <h2 className="text-3xl font-bold text-center mb-8">{t('home.features.title')}</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Link href="/mps" className="group">
            <div className="card-hover p-6 text-center h-full transform transition-all duration-300 group-hover:scale-105">
              <div className="w-16 h-16 mx-auto mb-4 bg-primary/10 rounded-full flex items-center justify-center group-hover:bg-primary/20 transition-colors">
                <svg className="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="font-bold mb-2">{t('home.features.mps.title')}</h3>
              <p className="text-sm text-muted-foreground">{t('home.features.mps.description')}</p>
              <ArrowRightIcon className="w-5 h-5 mx-auto mt-4 text-primary opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
          </Link>

          <Link href="/bills" className="group">
            <div className="card-hover p-6 text-center h-full transform transition-all duration-300 group-hover:scale-105">
              <div className="w-16 h-16 mx-auto mb-4 bg-primary/10 rounded-full flex items-center justify-center group-hover:bg-primary/20 transition-colors">
                <svg className="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 className="font-bold mb-2">{t('home.features.bills.title')}</h3>
              <p className="text-sm text-muted-foreground">{t('home.features.bills.description')}</p>
              <ArrowRightIcon className="w-5 h-5 mx-auto mt-4 text-primary opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
          </Link>

          <Link href="/debates" className="group">
            <div className="card-hover p-6 text-center h-full transform transition-all duration-300 group-hover:scale-105">
              <div className="w-16 h-16 mx-auto mb-4 bg-primary/10 rounded-full flex items-center justify-center group-hover:bg-primary/20 transition-colors">
                <svg className="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <h3 className="font-bold mb-2">{t('home.features.debates.title')}</h3>
              <p className="text-sm text-muted-foreground">{t('home.features.debates.description')}</p>
              <ArrowRightIcon className="w-5 h-5 mx-auto mt-4 text-primary opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
          </Link>

          <Link href="/committees" className="group">
            <div className="card-hover p-6 text-center h-full transform transition-all duration-300 group-hover:scale-105">
              <div className="w-16 h-16 mx-auto mb-4 bg-primary/10 rounded-full flex items-center justify-center group-hover:bg-primary/20 transition-colors">
                <svg className="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
              <h3 className="font-bold mb-2">{t('home.features.committees.title')}</h3>
              <p className="text-sm text-muted-foreground">{t('home.features.committees.description')}</p>
              <ArrowRightIcon className="w-5 h-5 mx-auto mt-4 text-primary opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
          </Link>
        </div>
      </div>
    </div>
    </>
  );
}