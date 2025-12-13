/**
 * AdGenesis - AI Design Assistant Component
 * Intelligent design assistant with suggestions, auto-generation, and improvements
 */

import React, { useState, useRef, useEffect } from 'react';
import { cn } from '../../lib/utils';
import './AIAssistant.css';

// Icons
const SparklesIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <path d="M10 2L11.5 6.5L16 8L11.5 9.5L10 14L8.5 9.5L4 8L8.5 6.5L10 2Z" fill="currentColor" />
    <path d="M15 12L15.75 14.25L18 15L15.75 15.75L15 18L14.25 15.75L12 15L14.25 14.25L15 12Z" fill="currentColor" opacity="0.7" />
    <path d="M5 12L5.5 13.5L7 14L5.5 14.5L5 16L4.5 14.5L3 14L4.5 13.5L5 12Z" fill="currentColor" opacity="0.5" />
  </svg>
);

const WandIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
    <path d="M11 3L15 7M3 11L11 3L15 7L7 15L3 11Z" />
    <path d="M9 5L13 9" />
  </svg>
);

const PaletteIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
    <circle cx="9" cy="9" r="7" />
    <circle cx="9" cy="5" r="1.5" fill="currentColor" />
    <circle cx="5.5" cy="8" r="1.5" fill="currentColor" />
    <circle cx="6.5" cy="12" r="1.5" fill="currentColor" />
    <path d="M12 9C12 10.5 11 12 9.5 12C10.5 12 12 11 12 9Z" fill="currentColor" />
  </svg>
);

const TypeIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
    <path d="M3 4H15" />
    <path d="M9 4V15" />
    <path d="M6 15H12" />
  </svg>
);

const LayoutIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
    <rect x="2" y="2" width="14" height="14" rx="2" />
    <path d="M2 7H16" />
    <path d="M7 7V16" />
  </svg>
);

const ImageIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
    <rect x="2" y="2" width="14" height="14" rx="2" />
    <circle cx="6" cy="6" r="1.5" />
    <path d="M16 12L12 8L6 14H14C15.1 14 16 13.1 16 12Z" />
  </svg>
);

const RefreshIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
    <path d="M2 9C2 5.13 5.13 2 9 2C12.87 2 16 5.13 16 9C16 12.87 12.87 16 9 16C6.5 16 4.32 14.62 3.17 12.5" />
    <path d="M2 14V10H6" />
  </svg>
);

const SendIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
    <path d="M16 2L9 9M16 2L11 16L9 9M16 2L2 7L9 9" />
  </svg>
);

const CloseIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <path d="M4 4L14 14M14 4L4 14" />
  </svg>
);

const ChevronIcon = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <path d="M6 4L10 8L6 12" />
  </svg>
);

// Quick action suggestions
const QUICK_SUGGESTIONS = [
  {
    id: 'generate-variations',
    icon: <RefreshIcon />,
    label: 'Generate variations',
    description: 'Create 4 different versions of this design',
    category: 'generate',
  },
  {
    id: 'improve-colors',
    icon: <PaletteIcon />,
    label: 'Improve color palette',
    description: 'Get AI-suggested color improvements',
    category: 'improve',
  },
  {
    id: 'fix-typography',
    icon: <TypeIcon />,
    label: 'Fix typography',
    description: 'Optimize font pairings and hierarchy',
    category: 'improve',
  },
  {
    id: 'auto-layout',
    icon: <LayoutIcon />,
    label: 'Auto-arrange layout',
    description: 'Apply professional layout principles',
    category: 'layout',
  },
  {
    id: 'suggest-images',
    icon: <ImageIcon />,
    label: 'Suggest images',
    description: 'Find relevant stock images',
    category: 'content',
  },
  {
    id: 'magic-resize',
    icon: <WandIcon />,
    label: 'Magic resize',
    description: 'Adapt design for multiple formats',
    category: 'export',
  },
];

// Example prompts
const EXAMPLE_PROMPTS = [
  'Make this design more modern and minimalist',
  'Add a gradient background with purple and blue tones',
  'Suggest better fonts for a tech startup',
  'Create a holiday-themed version',
  'Make the headline more impactful',
  'Add visual hierarchy to the content',
];

/**
 * AI Assistant Panel Component
 */
export const AIAssistant = ({
  isOpen,
  onClose,
  onApplySuggestion,
  currentDesign,
  className,
}) => {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [activeTab, setActiveTab] = useState('chat');
  const [history, setHistory] = useState([]);
  const inputRef = useRef(null);
  const chatEndRef = useRef(null);

  // Focus input when opened
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // Scroll to bottom of chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [history]);

  // Handle prompt submission
  const handleSubmit = async (e) => {
    e?.preventDefault();
    if (!prompt.trim() || isLoading) return;

    const userMessage = prompt.trim();
    setPrompt('');
    setHistory((prev) => [...prev, { type: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      // Simulate AI response (replace with actual API call)
      await new Promise((resolve) => setTimeout(resolve, 1500));
      
      const aiResponse = generateAIResponse(userMessage, currentDesign);
      setHistory((prev) => [...prev, { type: 'assistant', ...aiResponse }]);
      
      if (aiResponse.suggestions) {
        setSuggestions(aiResponse.suggestions);
      }
    } catch (error) {
      setHistory((prev) => [
        ...prev,
        {
          type: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.',
          error: true,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle quick suggestion click
  const handleQuickSuggestion = async (suggestion) => {
    setHistory((prev) => [
      ...prev,
      { type: 'user', content: suggestion.label },
    ]);
    setIsLoading(true);

    try {
      await new Promise((resolve) => setTimeout(resolve, 1500));
      
      const aiResponse = generateQuickResponse(suggestion, currentDesign);
      setHistory((prev) => [...prev, { type: 'assistant', ...aiResponse }]);
      
      if (aiResponse.action) {
        onApplySuggestion?.(aiResponse.action);
      }
    } catch (error) {
      // Handle error
    } finally {
      setIsLoading(false);
    }
  };

  // Clear chat history
  const handleClear = () => {
    setHistory([]);
    setSuggestions([]);
  };

  if (!isOpen) return null;

  return (
    <div className={cn('ai-assistant', className)}>
      {/* Header */}
      <div className="ai-assistant-header">
        <div className="ai-assistant-title">
          <div className="ai-icon-gradient">
            <SparklesIcon />
          </div>
          <div>
            <h3>AI Design Assistant</h3>
            <p>Powered by advanced AI</p>
          </div>
        </div>
        <button className="ai-close-btn" onClick={onClose}>
          <CloseIcon />
        </button>
      </div>

      {/* Tabs */}
      <div className="ai-tabs">
        <button
          className={cn('ai-tab', activeTab === 'chat' && 'ai-tab-active')}
          onClick={() => setActiveTab('chat')}
        >
          Chat
        </button>
        <button
          className={cn('ai-tab', activeTab === 'quick' && 'ai-tab-active')}
          onClick={() => setActiveTab('quick')}
        >
          Quick Actions
        </button>
        <button
          className={cn('ai-tab', activeTab === 'history' && 'ai-tab-active')}
          onClick={() => setActiveTab('history')}
        >
          History
        </button>
      </div>

      {/* Content */}
      <div className="ai-assistant-content">
        {activeTab === 'chat' && (
          <>
            {/* Chat Messages */}
            <div className="ai-chat">
              {history.length === 0 ? (
                <div className="ai-welcome">
                  <div className="ai-welcome-icon">
                    <SparklesIcon />
                  </div>
                  <h4>How can I help you today?</h4>
                  <p>
                    Ask me anything about your design. I can help with colors,
                    typography, layout, and more.
                  </p>
                  <div className="ai-example-prompts">
                    {EXAMPLE_PROMPTS.slice(0, 4).map((example, idx) => (
                      <button
                        key={idx}
                        className="ai-example-prompt"
                        onClick={() => setPrompt(example)}
                      >
                        {example}
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <>
                  {history.map((message, idx) => (
                    <div
                      key={idx}
                      className={cn(
                        'ai-message',
                        `ai-message-${message.type}`,
                        message.error && 'ai-message-error'
                      )}
                    >
                      {message.type === 'assistant' && (
                        <div className="ai-message-avatar">
                          <SparklesIcon />
                        </div>
                      )}
                      <div className="ai-message-content">
                        <p>{message.content}</p>
                        {message.suggestions && (
                          <div className="ai-message-suggestions">
                            {message.suggestions.map((sug, sIdx) => (
                              <button
                                key={sIdx}
                                className="ai-suggestion-chip"
                                onClick={() => onApplySuggestion?.(sug)}
                              >
                                {sug.label}
                                <ChevronIcon />
                              </button>
                            ))}
                          </div>
                        )}
                        {message.preview && (
                          <div className="ai-message-preview">
                            <img src={message.preview} alt="Preview" />
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                  {isLoading && (
                    <div className="ai-message ai-message-assistant">
                      <div className="ai-message-avatar">
                        <SparklesIcon />
                      </div>
                      <div className="ai-typing">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    </div>
                  )}
                  <div ref={chatEndRef} />
                </>
              )}
            </div>

            {/* Input */}
            <form className="ai-input-wrapper" onSubmit={handleSubmit}>
              <textarea
                ref={inputRef}
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Ask AI to help with your design..."
                className="ai-input"
                rows={1}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit();
                  }
                }}
              />
              <button
                type="submit"
                className="ai-send-btn"
                disabled={!prompt.trim() || isLoading}
              >
                <SendIcon />
              </button>
            </form>
          </>
        )}

        {activeTab === 'quick' && (
          <div className="ai-quick-actions">
            <p className="ai-quick-description">
              Quick actions for common design improvements
            </p>
            <div className="ai-quick-grid">
              {QUICK_SUGGESTIONS.map((suggestion) => (
                <button
                  key={suggestion.id}
                  className="ai-quick-action"
                  onClick={() => handleQuickSuggestion(suggestion)}
                  disabled={isLoading}
                >
                  <div className="ai-quick-icon">{suggestion.icon}</div>
                  <div className="ai-quick-info">
                    <span className="ai-quick-label">{suggestion.label}</span>
                    <span className="ai-quick-desc">{suggestion.description}</span>
                  </div>
                  <ChevronIcon />
                </button>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'history' && (
          <div className="ai-history">
            {history.length === 0 ? (
              <div className="ai-history-empty">
                <p>No conversation history yet</p>
                <span>Your AI interactions will appear here</span>
              </div>
            ) : (
              <>
                <button className="ai-clear-history" onClick={handleClear}>
                  Clear History
                </button>
                <div className="ai-history-list">
                  {history
                    .filter((m) => m.type === 'user')
                    .map((message, idx) => (
                      <div key={idx} className="ai-history-item">
                        <span>{message.content}</span>
                      </div>
                    ))}
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

// Helper function to generate AI response (mock - replace with actual API)
function generateAIResponse(prompt, design) {
  const lowerPrompt = prompt.toLowerCase();
  
  if (lowerPrompt.includes('color') || lowerPrompt.includes('palette')) {
    return {
      content: "I've analyzed your design and have some color suggestions. Here are professional palettes that would enhance your design:",
      suggestions: [
        { type: 'color', label: 'Apply Vibrant Palette', colors: ['#8B5CF6', '#06B6D4', '#F59E0B'] },
        { type: 'color', label: 'Apply Minimal Palette', colors: ['#1E293B', '#64748B', '#F8FAFC'] },
        { type: 'color', label: 'Apply Bold Palette', colors: ['#EF4444', '#0EA5E9', '#22C55E'] },
      ],
    };
  }
  
  if (lowerPrompt.includes('font') || lowerPrompt.includes('typography')) {
    return {
      content: "Here are some typography recommendations based on your design style:",
      suggestions: [
        { type: 'font', label: 'Modern Sans', fonts: ['Inter', 'SF Pro Display'] },
        { type: 'font', label: 'Classic Serif', fonts: ['Playfair Display', 'Lora'] },
        { type: 'font', label: 'Tech Style', fonts: ['Space Grotesk', 'JetBrains Mono'] },
      ],
    };
  }
  
  if (lowerPrompt.includes('layout') || lowerPrompt.includes('arrange')) {
    return {
      content: "I can help you improve the layout. Would you like me to:",
      suggestions: [
        { type: 'layout', label: 'Center all elements' },
        { type: 'layout', label: 'Apply grid layout' },
        { type: 'layout', label: 'Create visual hierarchy' },
      ],
    };
  }
  
  return {
    content: `I understand you want to "${prompt}". Let me analyze your design and provide some suggestions. Based on the current elements, I recommend focusing on visual hierarchy and ensuring your key message stands out.`,
    suggestions: [
      { type: 'action', label: 'Apply AI recommendations' },
      { type: 'action', label: 'Generate alternatives' },
    ],
  };
}

function generateQuickResponse(suggestion, design) {
  switch (suggestion.id) {
    case 'generate-variations':
      return {
        content: "I've generated 4 variations of your design. Each variation explores different approaches to your current concept.",
        action: { type: 'generate-variations', count: 4 },
      };
    case 'improve-colors':
      return {
        content: "I've analyzed the color psychology and accessibility of your design. Here are my recommendations:",
        action: { type: 'improve-colors' },
        suggestions: [
          { type: 'color', label: 'High Contrast', colors: ['#000000', '#FFFFFF', '#8B5CF6'] },
          { type: 'color', label: 'Soft Tones', colors: ['#F8FAFC', '#CBD5E1', '#6366F1'] },
        ],
      };
    case 'fix-typography':
      return {
        content: "Typography improvements applied! I've optimized font sizes for better hierarchy and readability.",
        action: { type: 'fix-typography' },
      };
    case 'auto-layout':
      return {
        content: "Layout optimized using professional design principles. Elements are now properly aligned with consistent spacing.",
        action: { type: 'auto-layout' },
      };
    case 'suggest-images':
      return {
        content: "Based on your design context, here are some image suggestions:",
        action: { type: 'suggest-images' },
      };
    case 'magic-resize':
      return {
        content: "Magic resize ready! Select the formats you want to export to:",
        action: { type: 'magic-resize' },
        suggestions: [
          { type: 'size', label: 'Instagram Post (1080×1080)' },
          { type: 'size', label: 'Instagram Story (1080×1920)' },
          { type: 'size', label: 'Facebook Cover (820×312)' },
          { type: 'size', label: 'Twitter Header (1500×500)' },
        ],
      };
    default:
      return {
        content: "I'm working on your request. This feature is being enhanced.",
      };
  }
}

/**
 * Floating AI Button Component
 */
export const AIFloatingButton = ({ onClick, className }) => {
  return (
    <button className={cn('ai-floating-btn', className)} onClick={onClick}>
      <SparklesIcon />
      <span>AI Assistant</span>
    </button>
  );
};

export default AIAssistant;
