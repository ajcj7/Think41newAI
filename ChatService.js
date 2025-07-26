import axios from 'axios'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Request interceptor for adding auth tokens, logging, etc.
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Log requests in development
    if (process.env.NODE_ENV === 'development') {
      console.log('API Request:', config.method?.toUpperCase(), config.url)
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Log errors in development
    if (process.env.NODE_ENV === 'development') {
      console.error('API Error:', error.response?.status, error.response?.data)
    }
    
    // Handle specific error cases
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token')
      // Optionally redirect to login
    }
    
    return Promise.reject(error)
  }
)

export const chatService = {
  // Start a new conversation
  async startConversation(userIdentifier = null) {
    try {
      const response = await api.post('/conversations/start', {
        user_identifier: userIdentifier || `anonymous_${Date.now()}`,
        channel: 'web'
      })
      return response.data
    } catch (error) {
      console.error('Failed to start conversation:', error)
      throw new Error('Failed to initialize chat session')
    }
  },

  // Send a message in the conversation
  async sendMessage(conversationId, message) {
    try {
      const response = await api.post('/conversations/message', {
        conversation_id: conversationId,
        message: message,
        sender: 'user'
      })
      return response.data
    } catch (error) {
      console.error('Failed to send message:', error)
      throw new Error('Failed to send message')
    }
  },

  // Get conversation history
  async getConversationHistory(conversationId) {
    try {
      const response = await api.get(`/conversations/${conversationId}/messages`)
      return response.data
    } catch (error) {
      console.error('Failed to get conversation history:', error)
      throw new Error('Failed to load conversation history')
    }
  },

  // Get top products
  async getTopProducts(limit = 5) {
    try {
      const response = await api.get(`/products/top?limit=${limit}`)
      return response.data
    } catch (error) {
      console.error('Failed to get top products:', error)
      throw new Error('Failed to load top products')
    }
  },

  // Get order status
  async getOrderStatus(orderId) {
    try {
      const response = await api.get(`/orders/${orderId}`)
      return response.data
    } catch (error) {
      console.error('Failed to get order status:', error)
      throw new Error('Failed to load order information')
    }
  },

  // Check product stock
  async checkProductStock(productName) {
    try {
      const response = await api.get(`/products/search?name=${encodeURIComponent(productName)}`)
      return response.data
    } catch (error) {
      console.error('Failed to check product stock:', error)
      throw new Error('Failed to check product availability')
    }
  },

  // Submit feedback for conversation
  async submitFeedback(conversationId, rating, feedback) {
    try {
      const response = await api.post('/conversations/feedback', {
        conversation_id: conversationId,
        rating: rating,
        feedback_text: feedback
      })
      return response.data
    } catch (error) {
      console.error('Failed to submit feedback:', error)
      throw new Error('Failed to submit feedback')
    }
  },

  // End conversation
  async endConversation(conversationId) {
    try {
      const response = await api.post(`/conversations/${conversationId}/end`)
      return response.data
    } catch (error) {
      console.error('Failed to end conversation:', error)
      // Don't throw error for this as it's not critical
    }
  }
}

// Mock service for development/testing
export const mockChatService = {
  async startConversation() {
    await new Promise(resolve => setTimeout(resolve, 500))
    return {
      conversation_id: `conv_${Date.now()}`,
      user_identifier: `user_${Date.now()}`,
      started_at: new Date().toISOString()
    }
  },

  async sendMessage(conversationId, message) {
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000))
    
    const lowerMessage = message.toLowerCase()
    
    // Mock responses based on message content
    if (lowerMessage.includes('top') && lowerMessage.includes('product')) {
      return {
        message: "Here are our top 5 most sold products:",
        type: 'products',
        data: [
          { id: 1, name: 'Classic T-Shirt', price: 19.99, total_sold: 150, stock_quantity: 100, category: 'Clothing' },
          { id: 2, name: 'Premium Hoodie', price: 49.99, total_sold: 120, stock_quantity: 50, category: 'Clothing' },
          { id: 3, name: 'Wireless Headphones', price: 99.99, total_sold: 95, stock_quantity: 25, category: 'Electronics' },
          { id: 4, name: 'Smart Watch', price: 199.99, total_sold: 80, stock_quantity: 15, category: 'Electronics' },
          { id: 5, name: 'Running Shoes', price: 79.99, total_sold: 75, stock_quantity: 30, category: 'Footwear' }
        ]
      }
    }
    
    if (lowerMessage.includes('order') && (lowerMessage.includes('status') || lowerMessage.includes('check'))) {
      return {
        message: "Please provide your order ID to check the status.",
        type: 'text'
      }
    }
    
    // Check for order ID pattern (numbers)
    const orderIdMatch = message.match(/\b\d{3,}\b/)
    if (orderIdMatch) {
      const orderId = orderIdMatch[0]
      return {
        message: `Here's the status of your order #${orderId}:`,
        type: 'order',
        data: {
          id: orderId,
          status: 'shipped',
          customer_name: 'John Doe',
          customer_email: 'john@example.com',
          total_amount: 69.98,
          created_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
          tracking_number: 'TRK123456789',
          items: [
            { product_name: 'Classic T-Shirt', quantity: 2, unit_price: 19.99, total_price: 39.98 },
            { product_name: 'Premium Hoodie', quantity: 1, unit_price: 29.99, total_price: 29.99 }
          ]
        }
      }
    }
    
    if (lowerMessage.includes('stock') || lowerMessage.includes('availability')) {
      return {
        message: "I can help you check product availability. Which product are you looking for?",
        type: 'text'
      }
    }
    
    if (lowerMessage.includes('help') || lowerMessage.includes('what can you')) {
      return {
        message: "I can help you with:\n\n• Check order status\n• View top selling products\n• Check product availability\n• Answer questions about shipping\n• Provide customer support\n\nWhat would you like to know?",
        type: 'text'
      }
    }
    
    // Default response
    return {
      message: "I understand you're asking about: \"" + message + "\"\n\nI can help you with order status, product information, and general support questions. Could you please be more specific about what you'd like to know?",
      type: 'text'
    }
  }
}

// Use mock service in development, real service in production
export default process.env.NODE_ENV === 'development' ? mockChatService : chatService
