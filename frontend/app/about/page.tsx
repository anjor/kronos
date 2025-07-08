import Link from 'next/link'
import { ArrowLeftIcon } from '@heroicons/react/24/outline'

export default function About() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <Link href="/" className="inline-flex items-center text-primary-600 hover:text-primary-700 mb-8">
          <ArrowLeftIcon className="h-5 w-5 mr-2" />
          Back to Home
        </Link>

        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="px-6 py-8 sm:px-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-6">
              Why I Built Kronos
            </h1>
            
            <div className="prose prose-lg prose-gray max-w-none">
              <p className="text-xl text-gray-600 mb-8">
                Hi, I&apos;m Anjor. I&apos;m a seasoned software engineer with over 10 years of experience 
                at companies like Palantir and Protocol Labs. Now I run an independent consulting practice 
                helping companies with AI systems and blockchain solutions. I lost a $5,000 client 
                because I double-booked a crucial meeting. That was my breaking point.
              </p>

              <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">
                The Problem That Drove Me Crazy
              </h2>
              <p className="text-gray-600 mb-6">
                As an independent consultant working with AI startups, Fortune 500 companies, and blockchain 
                projects, I juggle multiple clients across different industries. Each client has their 
                preferred scheduling tool:
              </p>
              <ul className="list-disc list-inside text-gray-600 mb-6 space-y-2">
                <li>AI startup clients use Google Calendar and book through Calendly</li>
                <li>Enterprise clients insist on Microsoft Teams with Outlook integration</li>
                <li>Blockchain projects found me through Cal.com and book everything there</li>
                <li>Personal appointments and technical interviews go in my main Google Calendar</li>
              </ul>
              <p className="text-gray-600 mb-6">
                I was constantly switching between four different calendar apps, manually cross-referencing 
                times, and still missing conflicts. The cognitive load was exhausting.
              </p>

              <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">
                The $5,000 Mistake
              </h2>
              <p className="text-gray-600 mb-6">
                In March 2024, I had a crucial client presentation about implementing an AI system 
                scheduled through Cal.com. At the same time, I had blocked my Google Calendar for 
                &quot;deep work&quot; but forgot to check if any meetings were actually booked during that time.
              </p>
              <p className="text-gray-600 mb-6">
                When I missed the presentation, the client interpreted it as unprofessional 
                and terminated our contract. That was a $5,000 project, plus the damage to 
                my reputation in the tight-knit AI consulting community.
              </p>

              <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">
                Existing Solutions Weren&apos;t Enough
              </h2>
              <p className="text-gray-600 mb-6">
                I tried everything:
              </p>
              <ul className="list-disc list-inside text-gray-600 mb-6 space-y-2">
                <li><strong>Zapier integrations:</strong> Complex to set up, broke frequently</li>
                <li><strong>Calendar sync tools:</strong> Only supported 2-way sync between major providers</li>
                <li><strong>Multiple calendar apps:</strong> None had real-time conflict detection</li>
                <li><strong>Personal assistants:</strong> Too expensive for an independent consultant</li>
              </ul>

              <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">
                Building the Solution I Needed
              </h2>
              <p className="text-gray-600 mb-6">
                After that expensive lesson, I decided to build the tool I wished existed. 
                Kronos does three things really well:
              </p>
              <ol className="list-decimal list-inside text-gray-600 mb-6 space-y-2">
                <li><strong>Universal sync:</strong> Connects Google, Microsoft, and Cal.com in one view</li>
                <li><strong>Conflict detection:</strong> Instantly alerts when meetings overlap</li>
                <li><strong>Client organization:</strong> Automatically tags meetings for invoicing</li>
              </ol>

              <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">
                The Results
              </h2>
              <p className="text-gray-600 mb-6">
                Since I started using Kronos for my own work:
              </p>
              <ul className="list-disc list-inside text-gray-600 mb-6 space-y-2">
                <li>Zero double-bookings in 6 months</li>
                <li>5 hours/week saved on calendar management</li>
                <li>Automatic time tracking for accurate invoicing</li>
                <li>Better client relationships due to reliability</li>
              </ul>

              <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">
                Why I&apos;m Sharing This
              </h2>
              <p className="text-gray-600 mb-6">
                I know I&apos;m not the only consultant dealing with calendar chaos. If you&apos;re 
                juggling multiple clients and scheduling tools, Kronos can save you the headache 
                (and expensive mistakes) I went through.
              </p>
              <p className="text-gray-600 mb-6">
                I&apos;m building this in public because I believe in transparency. You can follow 
                the development on <a href="https://github.com/anjor/kronos" className="text-primary-600 hover:text-primary-700">GitHub</a> 
                , see weekly progress updates, and even contribute ideas.
              </p>

              <div className="bg-primary-50 border-l-4 border-primary-400 p-6 mt-8">
                <p className="text-primary-800">
                  <strong>Ready to never double-book again?</strong> Join the waitlist and I&apos;ll 
                  send you early access as soon as it&apos;s ready.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-8 text-center">
          <Link href="/" className="btn-primary">
            Join the Waitlist
          </Link>
        </div>
      </div>
    </div>
  )
}