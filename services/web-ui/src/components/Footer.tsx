'use client';

import Link from 'next/link';
import { useTranslation } from '@/hooks/useTranslation';

export default function Footer() {
  const { t } = useTranslation();

  return (
    <footer className="mt-12 bg-muted/50 border-t border-border">
      <div className="content-container py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* About Section */}
          <div>
            <h3 className="font-bold mb-4 text-foreground">About OpenParliament</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/about" className="text-muted-foreground hover:text-foreground transition-colors">{t('common.footer.aboutUs')}</Link></li>
              <li><Link href="/api" className="text-muted-foreground hover:text-foreground transition-colors">{t('common.footer.api')}</Link></li>
              <li><Link href="/downloads" className="text-muted-foreground hover:text-foreground transition-colors">Bulk Downloads</Link></li>
              <li><a href="https://github.com/openparlca" className="text-muted-foreground hover:text-foreground transition-colors">{t('common.footer.sourceCode')}</a></li>
            </ul>
          </div>

          {/* Parliamentary Links */}
          <div>
            <h3 className="font-bold mb-4 text-foreground">Parliamentary Data</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/mps" className="text-muted-foreground hover:text-foreground transition-colors">{t('common.nav.mps')}</Link></li>
              <li><Link href="/bills" className="text-muted-foreground hover:text-foreground transition-colors">{t('common.nav.bills')}</Link></li>
              <li><Link href="/debates" className="text-muted-foreground hover:text-foreground transition-colors">{t('common.nav.debates')}</Link></li>
              <li><Link href="/committees" className="text-muted-foreground hover:text-foreground transition-colors">{t('common.nav.committees')}</Link></li>
            </ul>
          </div>

          {/* External Links */}
          <div>
            <h3 className="font-bold mb-4 text-foreground">External Resources</h3>
            <ul className="space-y-2 text-sm">
              <li><a href="https://www.ourcommons.ca" className="text-muted-foreground hover:text-foreground transition-colors">House of Commons</a></li>
              <li><a href="https://www.parl.ca/legisinfo" className="text-muted-foreground hover:text-foreground transition-colors">LEGISinfo</a></li>
              <li><a href="https://www.elections.ca" className="text-muted-foreground hover:text-foreground transition-colors">Elections Canada</a></li>
              <li><a href="https://represent.opennorth.ca" className="text-muted-foreground hover:text-foreground transition-colors">Represent API</a></li>
            </ul>
          </div>

          {/* Contact & Social */}
          <div>
            <h3 className="font-bold mb-4 text-foreground">Stay Connected</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/alerts" className="text-muted-foreground hover:text-foreground transition-colors">Email Alerts</Link></li>
              <li><Link href="/feeds/rss" className="text-muted-foreground hover:text-foreground transition-colors">RSS Feeds</Link></li>
              <li><a href="https://twitter.com/openparlca" className="text-muted-foreground hover:text-foreground transition-colors">Twitter</a></li>
              <li><Link href="/contact" className="text-muted-foreground hover:text-foreground transition-colors">{t('common.footer.contact')}</Link></li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-border text-center text-sm text-muted-foreground">
          <p>© 2025 OpenParliament.ca. {t('common.footer.allRightsReserved')}</p>
          <p className="mt-2">
            Data from the <a href="https://www.ourcommons.ca" className="text-primary hover:text-primary/80 transition-colors">House of Commons</a> under the 
            <a href="https://www.ourcommons.ca/en/open-data" className="text-primary hover:text-primary/80 transition-colors"> {t('common.footer.openData')}</a>.
          </p>
        </div>
      </div>
    </footer>
  );
}
