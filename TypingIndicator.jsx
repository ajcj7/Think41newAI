import React from 'react'
import { Bot } from 'lucide-react'

const TypingIndicator = () => {
  return (
    <div className="flex justify-start message-enter">
      <div className="flex items-start space-x-3 max-w-xs lg:max-w-md">
        {/* Bot Avatar */}
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center">
          <Bot size={16} className="text-gray-700" />
        </div>

        {/* Typing Animation */}
        <div className="bg-gray-200 text-gray-800 px-
