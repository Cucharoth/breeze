'use client';

import { useState, useRef, useEffect } from 'react';
import { MessageRead } from '../schemas/branch-schema';
import { branchApi } from '../api/branch-api';
import { toast } from 'sonner';
import { logger } from '@/lib/logger';

import { useScenario } from '@/features/scenarios/contexts/ScenarioContext';

import { messageApi } from '../api/message-api';

interface ChatProps {
  branchId: string;
  initialHistory: MessageRead[];
}

export default function Chat({ branchId, initialHistory }: ChatProps) {
  const { scenario } = useScenario();
  const actors = scenario?.character_profiles || [];
  
  const [messages, setMessages] = useState<MessageRead[]>(initialHistory);
  const [inputText, setInputText] = useState('');
  const [isGmMode, setIsGmMode] = useState(false);
  const [activeActor, setActiveActor] = useState(actors[0]?.name || 'Narrator');
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingContent, setStreamingContent] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleDelete = async (messageId: string) => {
    if (isStreaming) return;
    try {
      await messageApi.delete(messageId);
      setMessages(prev => prev.filter(m => m.id !== messageId));
      toast.info('The moment has been banished.');
    } catch (err) {
      toast.error('Failed to alter the past.');
    }
  };

  // Keep activeActor in sync with available actors from Context
  useEffect(() => {
    if (!isGmMode && activeActor !== 'Narrator' && !actors.find(a => a.name === activeActor)) {
      setActiveActor(actors[0]?.name || 'Narrator');
    }
  }, [actors, activeActor, isGmMode]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingContent]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      setIsGmMode(!isGmMode);
      toast.info(`Perspective: ${!isGmMode ? 'Game Master' : activeActor}`);
    }
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleRetry = async () => {
    if (isStreaming || messages.length === 0) return;
    
    // Check if the last message is from the assistant (the one to retry)
    const lastMsg = messages[messages.length - 1];
    if (lastMsg.role !== 'assistant') return;

    try {
      setIsStreaming(true);
      
      // 1. Delete the last message from DB and local state
      await branchApi.deleteLastMessage(branchId);
      setMessages(prev => prev.slice(0, -1));
      
      // 2. Trigger a fresh generation
      setStreamingContent('');
      const speaker = isGmMode ? 'Narrator' : activeActor;
      await branchApi.streamNext(branchId, speaker, (token) => {
        setStreamingContent(prev => prev + token);
      });
      
      const updatedHistory = await branchApi.getHistory(branchId);
      setMessages(updatedHistory);
      setStreamingContent('');
      
    } catch (err) {
      logger.error('Failed to retry generation:', err);
      toast.error('The manuscript could not be rewritten.');
    } finally {
      setIsStreaming(false);
    }
  };

  const handleSend = async () => {
    if (!inputText.trim() || isStreaming) return;

    // Use selected actor name if not in GM mode
    const userContent = isGmMode ? `Narrator: ${inputText}` : `${activeActor}: ${inputText}`;
    
    const userMessage: MessageRead = {
      id: Math.random().toString(36).substring(7),
      branch_id: branchId,
      role: 'user',
      content: userContent,
      created_at: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    
    try {
      setIsStreaming(true);
      setStreamingContent('');
      
      // Persist to DB before streaming
      await branchApi.addMessage(branchId, {
        role: userMessage.role,
        content: userMessage.content
      });
      
      const speaker = isGmMode ? 'Narrator' : activeActor;
      await branchApi.streamNext(branchId, speaker, (token) => {
        setStreamingContent(prev => prev + token);
      });
      
      const updatedHistory = await branchApi.getHistory(branchId);
      setMessages(updatedHistory);
      setStreamingContent('');
      
    } catch (err) {
      logger.error('Failed to stream response:', err);
      toast.error('The manuscript stopped writing.');
    } finally {
      setIsStreaming(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-stone-950">
      {/* Scrollable Messages Area */}
      <div className="flex-1 overflow-y-auto p-8 space-y-12 scrollbar-hide">
        <div className="max-w-3xl mx-auto space-y-12 pb-32">
          {messages.map((msg, idx) => (
            <div key={msg.id} className="group animate-in fade-in slide-in-from-bottom-4 duration-700">
              {msg.role === 'system' ? (
                <div className="relative py-8 px-12 border-y border-stone-800/30 bg-stone-900/10 italic text-stone-400 text-center font-serif leading-relaxed">
                   <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-stone-950 px-4">
                      <span className="h-1 w-1 rounded-full bg-stone-800 inline-block mb-1" />
                   </div>
                   {msg.content}
                   {idx === messages.length - 1 && !isStreaming && (
                      <button 
                        onClick={() => handleDelete(msg.id)}
                        className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-all text-[9px] text-stone-700 hover:text-red-900 uppercase font-bold tracking-widest px-1"
                        title="Banish this moment"
                      >
                        Banish
                      </button>
                   )}
                </div>
              ) : (
                <div className="flex items-start gap-4">
                  <div className={`mt-1.5 h-1.5 w-1.5 rounded-full ${msg.role === 'user' ? 'bg-stone-600' : 'bg-amber-600'}`} />
                  <div className="flex-1">
                      <div className="flex items-center justify-between mb-2">
                        <p className={`text-[10px] uppercase tracking-[0.2em] font-bold ${msg.role === 'user' ? 'text-stone-600' : 'text-amber-700/80'}`}>
                          {(() => {
                            const firstColonIndex = msg.content.indexOf(': ');
                            // Only treat as a label if the colon is near the start (under 30 chars)
                            if (firstColonIndex !== -1 && firstColonIndex < 30) {
                              return msg.content.substring(0, firstColonIndex);
                            }
                            return msg.role === 'user' ? 'You' : 'Narrator';
                          })()}
                        </p>
                        {idx === messages.length - 1 && !isStreaming && (
                          <button 
                            onClick={() => handleDelete(msg.id)}
                            className="opacity-0 group-hover:opacity-100 transition-all text-[9px] text-stone-700 hover:text-red-900 uppercase font-bold tracking-widest px-2 py-0.5 border border-stone-900 rounded"
                            title="Banish this moment"
                          >
                            Banish
                          </button>
                        )}
                      </div>
                      <div className="text-stone-300 leading-relaxed font-serif text-lg whitespace-pre-wrap">
                        {(() => {
                          const firstColonIndex = msg.content.indexOf(': ');
                          if (firstColonIndex !== -1 && firstColonIndex < 30) {
                            return msg.content.substring(firstColonIndex + 2);
                          }
                          return msg.content;
                        })()}
                      </div>
                  </div>
                </div>
              )}
            </div>
          ))}

          {isStreaming && (
            <div className="animate-pulse">
              <div className="flex items-start gap-4">
                <div className="mt-1.5 h-1.5 w-1.5 rounded-full bg-amber-600 shadow-[0_0_8px_rgba(217,119,6,0.5)]" />
                <div className="flex-1">
                   <p className="text-[10px] uppercase tracking-[0.2em] text-amber-600 mb-2 font-bold">The GM is writing...</p>
                   <div className="text-stone-300 leading-relaxed font-serif text-lg whitespace-pre-wrap">
                     {streamingContent}
                     <span className="inline-block w-1 h-5 bg-amber-600 ml-1 animate-bounce" />
                   </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <footer className="h-44 border-t border-stone-800/50 bg-stone-950/90 px-8 py-6 backdrop-blur-xl shrink-0">
        <div className="max-w-3xl mx-auto relative group">
          <div className="absolute -top-8 left-0 flex items-center gap-4">
            <div className="flex items-center gap-2">
               <span className={`text-[9px] uppercase tracking-widest font-bold px-2 py-0.5 rounded border border-stone-800 transition-colors ${isGmMode ? 'bg-amber-950/30 text-amber-500 border-amber-900/30' : 'bg-stone-900/50 text-stone-500'}`}>
                 {isGmMode ? 'Game Master' : 'Player'}
               </span>
            </div>
            
            {!isGmMode && actors.length > 0 && (
              <select 
                value={activeActor}
                onChange={(e) => setActiveActor(e.target.value)}
                className="bg-transparent border-none text-[10px] uppercase tracking-widest font-bold text-stone-400 focus:outline-none hover:text-amber-500 transition-colors cursor-pointer"
              >
                {actors.map(a => <option key={a.name} value={a.name} className="bg-stone-900">{a.name}</option>)}
              </select>
            )}
          </div>
          
          <textarea 
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            className="w-full h-24 bg-stone-900/30 border border-stone-800/50 rounded-xl p-4 text-stone-200 placeholder-stone-700 focus:outline-none focus:border-amber-900/30 focus:ring-1 focus:ring-amber-900/10 transition-all resize-none shadow-inner"
            placeholder={isGmMode ? "Describe a world event..." : `Speak as ${activeActor}...`}
            disabled={isStreaming}
          />
          
          <div className="absolute bottom-3 right-3 flex items-center gap-3">
            {messages.length > 0 && messages[messages.length - 1].role === 'assistant' && !isStreaming && (
              <button 
                onClick={handleRetry}
                className="text-[9px] text-stone-600 hover:text-amber-500 uppercase font-bold tracking-widest px-3 py-2 transition-colors border border-transparent hover:border-stone-800 rounded"
                title="Discard last response and try again"
              >
                Rewrite
              </button>
            )}
            <kbd className="hidden sm:block text-[9px] text-stone-700 border border-stone-800 rounded px-1.5 py-0.5 select-none">TAB to toggle GM</kbd>
            <button 
              onClick={handleSend}
              disabled={isStreaming || !inputText.trim()}
              className="bg-amber-800 hover:bg-amber-700 disabled:bg-stone-900 disabled:text-stone-700 text-amber-50 text-[10px] font-bold py-2 px-6 rounded-lg transition-all shadow-xl active:scale-95 uppercase tracking-widest"
            >
              {isStreaming ? 'WRITING...' : 'IGNITE'}
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}
