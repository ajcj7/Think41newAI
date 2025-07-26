import React, { useState, useRef, useEffect } from 'react'
import ChatMessage from './ChatMessage'
import ChatInput from './ChatInput'
import QuickActions from './QuickActions'
import TypingIndicator from './TypingIndicator'
import { chatService } from '../services/chatService'

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      message: 'Hello! I\'m your e-commerce assistant. How can I help you today?',
      timestamp: new Date(),
      type: 'text'
    }
  ])
  const [isTyping, setIsTyping] = useState(false)
  const [conversationId, setConversationId] = useState(null)
  const messagesEndRef = useRef(null)

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isTyping])

  // Initialize conversation on component mount
  useEffect(() => {
    initializeConversation()
  }, [])

  const initializeConversation = async () => {
    try {
      const response = await chatService.startConversation()
      setConversationId(response.conversation_id)
    } catch (error) {
      console.error('Failed to initialize conversation:', error)
    }
  }

  const handleSendMessage = async (messageText) => {
    if (!messageText.trim()) return

    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      sender: 'user',
      message: messageText,
      timestamp: new Date(),
      type: 'text'
    }

    setMessages(prev => [...prev, userMessage])
    setIsTyping(true)

    try {
      // Send message to backend
      const response = await chatService.sendMessage(conversationId, messageText)
      
      // Add bot response
      const botMessage = {
        id: Date.now() + 1,
        sender: 'bot',
        message: response.message,
        timestamp: new Date(),
        type: response.type || 'text',
        data: response.data // For structured responses (products, orders, etc.)
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Failed to send message:', error)
      
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        sender: 'bot',
        message: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
        type: 'error'
      }
      
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsTyping(false)
    }
  }

  const handleQuickAction = (action) => {
    handleSendMessage(action.message)
  }

  const quickActions = [
    {
      id: 'top-products',
      label: 'Top 5 Products',
      message: 'Show me the top 5 most sold products',
      icon: '🏆'
    },
    {
      id: 'order-status',
      label: 'Check Order',
      message: 'I want to check my order status',
      icon: '📦'
    },
    {
      id: 'stock-check',
      label: 'Stock Info',
      message: 'Check product availability',
      icon: '📊'
    },
    {
      id: 'help',
      label: 'Need Help',
      message: 'What can you help me with?',
      icon: '❓'
    }
  ]

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden h-[600px] flex flex-col">
      {/* Chat Header */}
      <div className="bg-primary-500 text-white p-4">
        <div className="flex items-center space-x-3">
          <div className="w-3 h-3 bg-green-400 rounded-full"></div>
          <div>
            <h3 className="font-semibold">Customer Support Assistant</h3>
            <p className="text-primary-100 text-sm">Online - Usually replies instantly</p>
          </div>
        </div>
      </div>

      {/* Quick Actions (shown when conversation is new) */}
      {messages.length <= 1 && (
        <QuickActions actions={quickActions} onActionClick={handleQuickAction} />
      )}

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        
        {/* Typing Indicator */}
        {isTyping && <TypingIndicator />}
        
        {/* Auto-scroll anchor */}
        <div ref={messagesEndRef} />
      </div>

      {/* Chat Input */}
      <ChatInput onSendMessage={handleSendMessage} disabled={isTyping} />
    </div>
  )
}

export default ChatInterface
