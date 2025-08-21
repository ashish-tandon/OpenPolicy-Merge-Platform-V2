import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  HomeIcon,
  ServerIcon,
  GlobeAltIcon,
  UserGroupIcon,
  DocumentTextIcon,
  ChartBarIcon,
  CogIcon,
  Bars3Icon,
  XMarkIcon,
  ChevronDownIcon,
  ChevronRightIcon,
  BoltIcon,
  WrenchScrewdriverIcon,
  UsersIcon,
  ShieldCheckIcon,
  BuildingOfficeIcon,
  ChatBubbleLeftRightIcon,
  ClockIcon,
  EyeIcon,
  BellIcon,
  PresentationChartLineIcon
} from '@heroicons/react/24/outline';
import UserProfile from '../auth/UserProfile';

export default function AdminNavigation() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [dataManagementOpen, setDataManagementOpen] = useState(true);
  const [parliamentaryDataOpen, setParliamentaryDataOpen] = useState(false);
  const [systemManagementOpen, setSystemManagementOpen] = useState(false);
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/', icon: HomeIcon },
    {
      name: 'Data Management',
      icon: GlobeAltIcon,
      open: dataManagementOpen,
      setOpen: setDataManagementOpen,
      children: [
        { name: 'Government Levels', href: '/data/government-levels', icon: BuildingOfficeIcon },
        { name: 'Jurisdictions', href: '/government/levels', icon: GlobeAltIcon },
        { name: 'Data Sources', href: '/data/sources', icon: ServerIcon },
        { name: 'Data Quality', href: '/data/quality', icon: EyeIcon }
      ]
    },
    {
      name: 'Parliamentary Data',
      icon: DocumentTextIcon,
      open: parliamentaryDataOpen,
      setOpen: setParliamentaryDataOpen,
      children: [
        { name: 'Debates', href: '/parliamentary/debates', icon: ChatBubbleLeftRightIcon },
        { name: 'Committees', href: '/parliamentary/committees', icon: UserGroupIcon },
        { name: 'Sessions', href: '/parliamentary/sessions', icon: ClockIcon },
        { name: 'Representatives', href: '/representatives', icon: UsersIcon },
        { name: 'Bills & Legislation', href: '/bills', icon: DocumentTextIcon },
        { name: 'Voting Records', href: '/votes', icon: ChartBarIcon }
      ]
    },
    {
      name: 'Notifications',
      icon: BellIcon,
      children: [
        { name: 'Setup & Configuration', href: '/admin/notifications', icon: CogIcon },
        { name: 'Statistics & Analytics', href: '/admin/notification-stats', icon: ChartBarIcon },
      ]
    },
    {
      name: 'System Management',
      icon: CogIcon,
      open: systemManagementOpen,
      setOpen: setSystemManagementOpen,
      children: [
        { name: 'ETL Management', href: '/etl', icon: WrenchScrewdriverIcon },
        { name: 'Scrapers Dashboard', href: '/scrapers', icon: BoltIcon },
        { name: 'Database Dashboard', href: '/database', icon: ServerIcon },
        { name: 'API Gateway', href: '/api-gateway', icon: ServerIcon },
        { name: 'Website Analytics', href: '/analytics', icon: PresentationChartLineIcon },
        { name: 'System Monitoring', href: '/monitoring', icon: EyeIcon },
        { name: 'User Management', href: '/users', icon: ShieldCheckIcon },
        { name: 'System Settings', href: '/settings', icon: CogIcon }
      ]
    }
  ];

  const isActive = (href: string) => {
    if (href === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(href);
  };

  return (
    <>
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 z-50 lg:hidden ${sidebarOpen ? 'block' : 'hidden'}`}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />
        <div className="fixed inset-y-0 left-0 flex w-64 flex-col bg-white">
          <div className="flex h-16 items-center justify-between px-4">
            <h1 className="text-xl font-semibold text-gray-900">OpenPolicy Admin</h1>
            <button
              onClick={() => setSidebarOpen(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              <XMarkIcon className="h-6 w-6" />
            </button>
          </div>
          <nav className="flex-1 space-y-1 px-2 py-4">
            {navigation.map((item) => (
              <div key={item.name}>
                {item.children ? (
                  <div>
                    <button
                      onClick={() => item.setOpen(!item.open)}
                      className={`group flex w-full items-center px-2 py-2 text-sm font-medium rounded-md ${
                        item.open ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                      }`}
                    >
                      <item.icon className="mr-3 h-5 w-5 flex-shrink-0" />
                      {item.name}
                      {item.open ? (
                        <ChevronDownIcon className="ml-auto h-4 w-4" />
                      ) : (
                        <ChevronRightIcon className="ml-auto h-4 w-4" />
                      )}
                    </button>
                    {item.open && (
                      <div className="ml-4 space-y-1">
                        {item.children.map((child) => (
                          <Link
                            key={child.name}
                            to={child.href}
                            className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                              isActive(child.href)
                                ? 'bg-op-blue text-white'
                                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                            }`}
                            onClick={() => setSidebarOpen(false)}
                          >
                            <child.icon className="mr-3 h-4 w-4 flex-shrink-0" />
                            {child.name}
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>
                ) : (
                  <Link
                    to={item.href}
                    className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                      isActive(item.href)
                        ? 'bg-op-blue text-white'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                    onClick={() => setSidebarOpen(false)}
                  >
                    <item.icon className="mr-3 h-5 w-5 flex-shrink-0" />
                    {item.name}
                  </Link>
                )}
              </div>
            ))}
          </nav>
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
        <div className="flex flex-col flex-grow bg-white border-r border-gray-200">
          <div className="flex h-16 items-center justify-between px-4 border-b border-gray-200">
            <div className="flex items-center">
              <img
                src="/assets/images/logo.svg"
                alt="OpenPolicy"
                className="h-8 w-auto mr-2"
              />
              <h1 className="text-lg font-semibold text-gray-900">Admin</h1>
            </div>
          </div>
          
          {/* User Profile Section */}
          <div className="px-4 py-3 border-b border-gray-200">
            <UserProfile />
          </div>
          <nav className="flex-1 space-y-1 px-2 py-4">
            {navigation.map((item) => (
              <div key={item.name}>
                {item.children ? (
                  <div>
                    <button
                      onClick={() => item.setOpen(!item.open)}
                      className={`group flex w-full items-center px-2 py-2 text-sm font-medium rounded-md ${
                        item.open ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                      }`}
                    >
                      <item.icon className="mr-3 h-5 w-5 flex-shrink-0" />
                      {item.name}
                      {item.open ? (
                        <ChevronDownIcon className="ml-auto h-4 w-4" />
                      ) : (
                        <ChevronRightIcon className="ml-auto h-4 w-4" />
                      )}
                    </button>
                    {item.open && (
                      <div className="ml-4 space-y-1">
                        {item.children.map((child) => (
                          <Link
                            key={child.name}
                            to={child.href}
                            className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                              isActive(child.href)
                                ? 'bg-op-blue text-white'
                                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                            }`}
                          >
                            <child.icon className="mr-3 h-4 w-4 flex-shrink-0" />
                            {child.name}
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>
                ) : (
                  <Link
                    to={item.href}
                    className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                      isActive(item.href)
                        ? 'bg-op-blue text-white'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                  >
                    <item.icon className="mr-3 h-5 w-5 flex-shrink-0" />
                    {item.name}
                  </Link>
                )}
              </div>
            ))}
          </nav>
        </div>
      </div>

      {/* Mobile menu button */}
      <div className="lg:hidden">
        <button
          onClick={() => setSidebarOpen(true)}
          className="fixed top-4 left-4 z-40 p-2 rounded-md bg-white shadow-lg border border-gray-200"
        >
          <Bars3Icon className="h-6 w-6 text-gray-600" />
        </button>
      </div>
    </>
  );
}
