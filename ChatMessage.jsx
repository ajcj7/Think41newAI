import React from 'react'
import { Bot, User } from 'lucide-react'
import { format } from 'date-fns'
import ProductList from './ProductList'
import OrderInfo from './OrderInfo'

const ChatMessage = ({ message }) => {
  const isUser = message.sender === 'user'
  const isBot = message.sender === 'bot'

  const formatTime = (timestamp) => {
    return format(new Date(timestamp), 'HH:mm')
  }

  const renderMessageContent = () => {
    switch (message.type) {
      case 'products':
        return <ProductList products={message.data} />
      case 'order':
        return <OrderInfo order={message.data} />
      case 'error':
        return (
          <div className="text-red-600 bg-red-50 p-3 rounded-lg">
            <p>{message.message}</p>
          </div>
        )
      default:
        return (
          <div className={`message-bubble ${isUser ? 'user-message' : 'bot-message'}`}>
            <p className="whitespace-pre-wrap">{message.message}</p>
          </div>
        )
    }
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} message-enter`}>
      <div className={`flex items-start space-x-3 max-w-xs lg:max-w-md ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? 'bg-primary-500' : 'bg-gray-300'
        }`}>
          {isUser ? (
            <User size={16} className="text-white" />
          ) : (
            <Bot size={16} className="text-gray-700" />
          )}
        </div>

        {/* Message Content */}
        <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
          {renderMessageContent()}
          
          {/* Timestamp */}
          <span className="text-xs text-gray-500 mt-1">
            {formatTime(message.timestamp)}
          </span>
        </div>
      </div>
    </div>
  )
}

export default ChatMessage
