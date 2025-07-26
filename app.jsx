import React from 'react'
import ChatInterface from './components/ChatInterface'
import Header from './components/Header'
import { MessageCircle } from 'lucide-react'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-500 to-primary-700 text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <div className="flex justify-center mb-6">
            <MessageCircle size={64} className="text-white" />
          </div>
          <h1 className="text-4xl font-bold mb-4">
            E-Commerce Support Assistant
          </h1>
          <p className="text-xl text-primary-100 max-w-2xl mx-auto">
            Get instant help with your orders, product information, and shopping questions. 
            Our AI assistant is here 24/7 to help you.
          </p>
        </div>
      </div>

      {/* Chat Interface */}
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <ChatInterface />
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8 mt-16">
        <div className="container mx-auto px-4 text-center">
          <p>&copy; 2024 E-Commerce Support. All rights reserved.</p>
          <p className="text-gray-400 mt-2">
            Powered by AI • Available 24/7 • Instant Responses
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
