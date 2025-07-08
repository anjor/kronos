import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { email } = await request.json()
    
    if (!email || !email.includes('@')) {
      return NextResponse.json(
        { error: 'Valid email is required' },
        { status: 400 }
      )
    }

    // For now, we'll just log the email and return success
    // In production, you'd save this to a database
    console.log('Waitlist signup:', email)
    
    // Mock response with waitlist position
    const waitlistPosition = Math.floor(Math.random() * 50) + 100
    
    return NextResponse.json(
      { 
        success: true, 
        message: 'Successfully joined waitlist',
        position: waitlistPosition
      },
      { status: 200 }
    )
  } catch (error) {
    console.error('Waitlist signup error:', error)
    return NextResponse.json(
      { error: 'Failed to join waitlist' },
      { status: 500 }
    )
  }
}