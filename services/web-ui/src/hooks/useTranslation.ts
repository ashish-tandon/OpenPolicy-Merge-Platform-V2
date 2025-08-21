import { useRouter } from 'next/navigation'
import { useCallback, useEffect, useState } from 'react'
import en from '@/locales/en'
import fr from '@/locales/fr'
import { getStoredLanguage, setStoredLanguage } from '@/lib/preferences'

type Translations = typeof en

const translations: Record<string, Translations> = {
  en,
  fr,
}

export function useTranslation() {
  const router = useRouter()
  const [locale, setLocale] = useState(getStoredLanguage())

  useEffect(() => {
    const handleStorageChange = () => {
      setLocale(getStoredLanguage())
    }

    window.addEventListener('storage', handleStorageChange)
    return () => window.removeEventListener('storage', handleStorageChange)
  }, [])

  const t = useCallback((key: string, params?: Record<string, any>) => {
    const keys = key.split('.')
    let value: any = translations[locale]
    
    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) {
        value = value[k]
      } else {
        console.warn(`Translation key not found: ${key}`)
        return key
      }
    }

    if (typeof value === 'string' && params) {
      return value.replace(/\{\{(\w+)\}\}/g, (match, param) => {
        return params[param]?.toString() || match
      })
    }

    return value || key
  }, [locale])

  const changeLanguage = useCallback((newLocale: string) => {
    setStoredLanguage(newLocale)
    setLocale(newLocale)
    router.refresh()
  }, [router])

  return {
    t,
    locale,
    changeLanguage,
  }
}