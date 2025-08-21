'use client';

import { useState, useEffect, useRef } from 'react';
import { 
  ChatBubbleLeftRightIcon,
  PaperAirplaneIcon,
  LightBulbIcon,
  UserIcon,
  ComputerDesktopIcon
} from '@heroicons/react/24/outline';
import { api } from '@/lib/api';

interface BillChatProps {
  billNumber: string;
  billTitle: string;
  billSummary?: string;
  userId?: string;
}

interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

export default function BillChat({ billNumber, billTitle, billSummary, userId }: BillChatProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Load initial bill information and suggestions
    loadBillInfo();
    loadChatSuggestions();
  }, [billNumber]);

  useEffect(() => {
    // Auto-scroll to bottom when new messages arrive
    scrollToBottom();
  }, [messages]);

  const loadBillInfo = async () => {
    try {
      const response = await api.getBillForChat(billNumber);
      if (response.success && response.data) {
        const billData = response.data;
        // Add initial AI message with bill summary
        const initialMessage: ChatMessage = {
          id: 'initial',
          text: `I can help you understand Bill ${billNumber}: ${billData.title}. ${billData.summary}`,
          sender: 'ai',
          timestamp: new Date()
        };
        setMessages([initialMessage]);
      }
    } catch (_error) {
      console.error('Error loading bill info:', error);
      // Add fallback message
      const fallbackMessage: ChatMessage = {
        id: 'fallback',
        text: `I can help you understand Bill ${billNumber}: ${billTitle}. What would you like to know about this bill?`,
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages([fallbackMessage]);
    }
  };

  const loadChatSuggestions = async () => {
    try {
      const response = await api.getChatSuggestions(billNumber);
      if (response.success) {
        setSuggestions(response.suggestions);
      }
    } catch (_error) {
      console.error('Error loading suggestions:', error);
      // Fallback suggestions
      setSuggestions([
        `Explain Bill ${billNumber} to me`,
        `What are the key points of Bill ${billNumber}?`,
        `How will Bill ${billNumber} affect me?`,
        `What's apos;s the current status of Bill ${billNumber}?`
      ]);
    }
  };

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      text: text.trim(),
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setShowSuggestions(false);
    setIsLoading(true);

    try {
      const response = await api.billChat(
        billNumber,
        billSummary || billTitle,
        text.trim()
      );

      if (response.success) {
        const aiMessage: ChatMessage = {
          id: (Date.now() + 1).toString(),
          text: response.response,
          sender: 'ai',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error('Failed to get AI response');
      }
    } catch (_error) {
      console.error('Error sending message:', error);
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInputText(suggestion);
    handleSendMessage(suggestion);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      {/* Chat Header */}
      <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <div className="flex items-center space-x-3">
          <ChatBubbleLeftRightIcon className="h-6 w-6 text-op-blue" />
          <div>
            <h3 className="text-lg font-medium text-gray-900">AI Chat Assistant</h3>
            <p className="text-sm text-gray-600">
              Ask questions about Bill {billNumber}: {billTitle}
            </p>
          </div>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="h-96 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                message.sender === 'user'
                  ? 'bg-op-blue text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              <div className="flex items-start space-x-2">
                {message.sender === 'user' ? (
                  <UserIcon className="h-4 w-4 mt-0.5 flex-shrink-0" />
                ) : (
                  <ComputerDesktopIcon className="h-4 w-4 mt-0.5 flex-shrink-0" />
                )}
                <div className="flex-1">
                  <p className="text-sm leading-relaxed">{message.text}</p>
                  <p className={`text-xs mt-1 ${
                    message.sender === 'user' ? 'text-op-blue-100' : 'text-gray-500'
                  }`}>
                    {formatTime(message.timestamp)}
                  </p>
                </div>
              </div>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-900 px-4 py-2 rounded-lg">
              <div className="flex items-center space-x-2">
                <ComputerDesktopIcon className="h-4 w-4" />
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Chat Suggestions */}
      {showSuggestions && suggestions.length > 0 && (
        <div className="px-4 pb-4 border-t border-gray-200 pt-4">
          <div className="flex items-center space-x-2 mb-3">
            <LightBulbIcon className="h-4 w-4 text-yellow-500" />
            <span className="text-sm font-medium text-gray-700">Suggested Questions</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {suggestions.slice(0, 4).map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(suggestion)}
                className="px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Chat Input */}
      <div className="px-4 pb-4 border-t border-gray-200 pt-4">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage(inputText)}
            placeholder="Ask anything about this bill..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue"
            disabled={isLoading}
          />
          <button
            onClick={() => handleSendMessage(inputText)}
            disabled={!inputText.trim() || isLoading}
            className="px-4 py-2 bg-op-blue text-white rounded-lg hover:bg-op-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <PaperAirplaneIcon className="h-4 w-4" />
          </button>
        </div>
        
        {!showSuggestions && (
          <button
            onClick={() => setShowSuggestions(true)}
            className="mt-2 text-sm text-op-blue hover:text-op-blue-700 transition-colors"
          >
            Show suggestions
          </button>
        )}
      </div>

      {/* Chat Info */}
      <div className="px-4 py-3 bg-gray-50 border-t border-gray-200">
        <p className="text-xs text-gray-500 text-center">
          AI responses are for informational purposes only. For official information, please consult government sources.
        </p>
      </div>
    </div>
  );
}
