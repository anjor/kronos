'use client'

import { useState } from 'react'
import Link from 'next/link'
import { CalendarDaysIcon, ClockIcon, UserGroupIcon, CheckCircleIcon } from '@heroicons/react/24/outline'

export default function Home() {
  const [email, setEmail] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setError('')

    try {
      const response = await fetch('/api/waitlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      })

      if (response.ok) {
        setIsSubmitted(true)
        setEmail('')
      } else {
        setError('Something went wrong. Please try again.')
      }
    } catch (err) {
      setError('Unable to join waitlist. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="py-12">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
              <span className="block">Never Double-Book</span>
              <span className="block text-primary-600">Client Meetings Again</span>
            </h1>
            <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
              I built Kronos after losing a $5k client to a scheduling conflict. 
              Now it syncs all my calendars and saves me 5 hours every week.
            </p>
          </div>

          {/* Waitlist Form */}
          <div className="mt-10 max-w-md mx-auto">
            {!isSubmitted ? (
              <form onSubmit={handleSubmit} className="sm:flex">
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  className="w-full px-5 py-3 border border-gray-300 shadow-sm placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 rounded-md"
                />
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="mt-3 w-full sm:mt-0 sm:ml-3 sm:w-auto sm:flex-shrink-0 px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
                >
                  {isSubmitting ? 'Joining...' : 'Join Waitlist'}
                </button>
              </form>
            ) : (
              <div className="text-center p-6 bg-green-50 rounded-lg">
                <CheckCircleIcon className="h-12 w-12 text-green-600 mx-auto mb-3" />
                <h3 className="text-lg font-medium text-green-900">You&apos;re on the list!</h3>
                <p className="mt-1 text-sm text-green-700">
                  I&apos;ll send you weekly updates as I build Kronos in public.
                </p>
              </div>
            )}
            {error && (
              <p className="mt-2 text-sm text-red-600 text-center">{error}</p>
            )}
            <p className="mt-3 text-xs text-gray-500 text-center">
              Join 127 freelancers waiting for early access. No spam, unsubscribe anytime.
            </p>
          </div>

          {/* Features */}
          <div className="mt-20">
            <h2 className="text-center text-3xl font-bold text-gray-900 mb-12">
              One Tool to Rule All Your Calendars
            </h2>
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white mx-auto">
                  <CalendarDaysIcon className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-lg font-medium text-gray-900 text-center">
                  Multi-Calendar Sync
                </h3>
                <p className="mt-2 text-sm text-gray-500 text-center">
                  Connect Google Calendar, Microsoft Calendar, and Cal.com. See everything in one view.
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
                  Get instant alerts when meetings overlap. Never apologize for double-booking again.
                </p>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white mx-auto">
                  <UserGroupIcon className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-lg font-medium text-gray-900 text-center">
                  Client Organization
                </h3>
                <p className="mt-2 text-sm text-gray-500 text-center">
                  Tag meetings by client. Track time automatically. Invoice with confidence.
                </p>
              </div>
            </div>
          </div>

          {/* Building in Public Section */}
          <div className="mt-20 bg-white rounded-lg shadow-md p-8 max-w-3xl mx-auto">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              🚀 Building in Public
            </h2>
            <div className="prose prose-gray">
              <p className="text-gray-600">
                I&apos;m building Kronos to solve my own calendar chaos as a freelancer juggling multiple clients.
                After years of missed meetings and scheduling conflicts, I decided to build the tool I wished existed.
              </p>
              <ul className="mt-4 space-y-2 text-gray-600">
                <li>✅ Week 1: Basic calendar sync working (Google Calendar connected!)</li>
                <li>✅ Week 2: Conflict detection algorithm implemented</li>
                <li>🔄 Week 3: Adding Microsoft Calendar integration</li>
                <li>⏳ Week 4: Beta launch to first 10 users</li>
              </ul>
              <p className="mt-4 text-gray-600">
                Follow the journey on <a href="https://twitter.com/yourhandle" className="text-primary-600 hover:text-primary-700">Twitter</a> or 
                {' '}<a href="https://github.com/anjor/kronos" className="text-primary-600 hover:text-primary-700">GitHub</a>.
              </p>
            </div>
          </div>

          {/* Bottom CTA */}
          <div className="mt-16 text-center">
            <p className="text-lg text-gray-600 mb-8">
              Ready to take control of your schedule?
            </p>
            <a href="#" onClick={(e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); }} className="btn-primary">
              Join the Waitlist
            </a>
            <Link href="/about" className="btn-secondary ml-4">
              My Story
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}