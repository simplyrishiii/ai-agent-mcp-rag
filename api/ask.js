export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return res.status(503).json({
      error: 'AI API is not configured yet. Add GEMINI_API_KEY to the Vercel project environment variables.'
    });
  }

  try {
    const { question, context } = req.body || {};
    if (!question || typeof question !== 'string') {
      return res.status(400).json({ error: 'A question is required.' });
    }

    const prompt = `You are the generation and verification stage of an AI-agent portfolio demo. Answer the user's question using only the supplied retrieved context when it is relevant. Be concise, technically accurate, and explicitly say when the context is insufficient. Do not invent citations.\n\nUser question:\n${question}\n\nRetrieved context:\n${context || '(none)'}`;

    const response = await fetch(
      'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=' + encodeURIComponent(apiKey),
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: { temperature: 0.2, maxOutputTokens: 500 }
        })
      }
    );

    const data = await response.json();
    if (!response.ok) {
      return res.status(response.status).json({
        error: data?.error?.message || 'Gemini API request failed.'
      });
    }

    const answer = data?.candidates?.[0]?.content?.parts?.map(p => p.text || '').join('').trim();
    if (!answer) return res.status(502).json({ error: 'The model returned an empty response.' });

    return res.status(200).json({ answer, provider: 'Google Gemini' });
  } catch (error) {
    return res.status(500).json({ error: 'AI request failed. Please try again.' });
  }
}
