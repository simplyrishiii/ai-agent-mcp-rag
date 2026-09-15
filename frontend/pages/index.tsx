import React, { useState } from 'react';
import axios from 'axios';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: Array<{ content: string; score: number }>;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [useMCP, setUseMCP] = useState(false);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000/api';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim()) return;

    // Add user message
    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(`${apiUrl}/query`, {
        query: input,
        use_mcp: useMCP,
        top_k: 5
      });

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.answer,
        sources: response.data.sources
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, there was an error processing your request. Please try again.'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <div className="max-w-4xl mx-auto h-screen flex flex-col">
        {/* Header */}
        <div className="bg-slate-800/50 backdrop-blur border-b border-slate-700/50 p-6">
          <h1 className="text-3xl font-bold text-white mb-2">
            AI Agent with MCP & RAG
          </h1>
          <p className="text-slate-300">
            Intelligent retrieval-augmented generation powered by LangChain
          </p>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 && (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <div className="text-6xl mb-4">🤖</div>
                <h2 className="text-2xl font-bold text-white mb-2">
                  Welcome to AI Agent
                </h2>
                <p className="text-slate-400">
                  Ask anything and get answers backed by reliable sources
                </p>
              </div>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div
                className={`max-w-2xl p-4 rounded-lg ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-700/50 text-slate-100 border border-slate-600'
                }`}
              >
                <p className="mb-2">{msg.content}</p>
                
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-slate-600">
                    <p className="text-xs font-semibold text-slate-300 mb-2">Sources:</p>
                    <div className="space-y-1">
                      {msg.sources.map((source, sidx) => (
                        <div key={sidx} className="text-xs text-slate-400">
                          📎 {source.content.substring(0, 50)}... (confidence: {(source.score * 100).toFixed(0)}%)
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-slate-700/50 text-slate-100 p-4 rounded-lg border border-slate-600">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-100"></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-200"></div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="bg-slate-800/50 backdrop-blur border-t border-slate-700/50 p-6">
          <form onSubmit={handleSubmit} className="space-y-3">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask me anything..."
                disabled={loading}
                className="flex-1 bg-slate-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              />
              <button
                type="submit"
                disabled={loading || !input.trim()}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                {loading ? 'Thinking...' : 'Send'}
              </button>
            </div>
            
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="mcp-toggle"
                checked={useMCP}
                onChange={(e) => setUseMCP(e.target.checked)}
                disabled={loading}
                className="w-4 h-4 cursor-pointer"
              />
              <label htmlFor="mcp-toggle" className="text-sm text-slate-300 cursor-pointer">
                Use MCP Tools
              </label>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}