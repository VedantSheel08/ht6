import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const data = await req.json();
    console.log('Logged response:', data);

    // Send to imaginary API
    try {
      await fetch('https://imaginary.api/endpoint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
    } catch (apiError) {
      console.error('Failed to send to imaginary API:', apiError);
    }

    return NextResponse.json({ status: 'ok' });
  } catch (error) {
    console.error('Error logging response:', error);
    return NextResponse.json({ status: 'error', error: error?.toString?.() });
  }
} 