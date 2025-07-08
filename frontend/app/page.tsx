import Link from 'next/link'
import { CalendarDaysIcon, ClockIcon, UserGroupIcon } from '@heroicons/react/24/outline'

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="py-12">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
              <span className="block">Kronos</span>
              <span className="block text-primary-600">Calendar Management</span>
            </h1>
            <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
              Sync events from Google Calendar, Microsoft Calendar, and Cal.com. 
              Detect conflicts and manage your availability seamlessly.
            </p>
          </div>

          <div className="mt-16">
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white mx-auto">
                  <CalendarDaysIcon className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-lg font-medium text-gray-900 text-center">
                  Multi-Calendar Sync
                </h3>
                <p className="mt-2 text-sm text-gray-500 text-center">
                  Connect Google Calendar, Microsoft Calendar, and Cal.com in one place
                </p>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white mx-auto">
                  <ClockIcon className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-lg font-medium text-gray-900 text-center">
                  Conflict Detection
                </h3>
                <p className="mt-2 text-sm text-gray-500 text-center">
                  Automatically detect and resolve scheduling conflicts
                </p>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white mx-auto">
                  <UserGroupIcon className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-lg font-medium text-gray-900 text-center">
                  Client Management
                </h3>
                <p className="mt-2 text-sm text-gray-500 text-center">
                  Organize events by clients and projects
                </p>
              </div>
            </div>
          </div>

          <div className="mt-16 text-center">
            <Link href="/auth/login" className="btn-primary mr-4">
              Get Started
            </Link>
            <Link href="/api/docs" className="btn-secondary">
              API Documentation
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}