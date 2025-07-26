# E-Commerce Chatbot Frontend

A modern, responsive React-based frontend for an e-commerce customer support chatbot.

## 🚀 Features

- **Real-time Chat Interface** - Smooth, responsive chat experience
- **Quick Action Buttons** - Get started with common queries instantly
- **Product Display** - Rich product cards with images and details
- **Order Tracking** - Visual order status with tracking information
- **Typing Indicators** - Shows when the bot is responding
- **Mobile Responsive** - Works perfectly on all devices
- **Mock Service** - Development mode with realistic mock responses

## 📁 Project Structure

```
frontend/
├── public/
│   └── vite.svg
├── src/
│   ├── components/
│   │   ├── ChatInterface.jsx     # Main chat container
│   │   ├── ChatMessage.jsx       # Individual message component
│   │   ├── ChatInput.jsx         # Message input with send button
│   │   ├── Header.jsx            # Navigation header
│   │   ├── QuickActions.jsx      # Quick action buttons
│   │   ├── TypingIndicator.jsx   # Bot typing animation
│   │   ├── ProductList.jsx       # Product display component
│   │   └── OrderInfo.jsx         # Order status display
│   ├── services/
│   │   └── chatService.js        # API service layer
│   ├── App.jsx                   # Main app component
│   ├── main.jsx                  # React entry point
│   └── index.css                 # Global styles with Tailwind
├── index.html                    # HTML template
├── package.json                  # Dependencies and scripts
├── vite.config.js               # Build configuration
├── tailwind.config.js           # Tailwind CSS configuration
└── README.md                    # This file
```

## 🛠️ Installation

1. **Clone and navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to `http://localhost:3000`

## 📦 Dependencies

### Core Dependencies
- **React 18** - UI library
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API requests
- **Lucide React** - Beautiful icon library
- **date-fns** - Date formatting utilities

### Development Dependencies
- **ESLint** - Code linting
- **PostCSS** - CSS processing
- **Autoprefixer** - CSS vendor prefixes

## 🎨 Styling

The project uses **Tailwind CSS** for styling with custom configurations:

- **Custom Colors** - Primary blue theme with gray accents
- **Animations** - Smooth transitions and loading states
- **Responsive Design** - Mobile-first approach
- **Custom Components** - Reusable button and message styles

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the frontend root:

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_NODE_ENV=development
```

### API Integration
The chatbot connects to your backend API through:

- **Base URL**: `/api` (proxied to `http://localhost:8000` in development)
- **Endpoints**:
  - `POST /conversations/start` - Initialize conversation
  - `POST /conversations/message` - Send user message
  - `GET /products/top` - Get top selling products
  - `GET /orders/{id}` - Get order status

## 🧪 Development Mode

The app includes a **mock service** for development that provides realistic responses:

- **Top Products Query** - Returns sample product data
- **Order Status Check** - Shows order tracking information
- **Stock Inquiries** - Product availability responses
- **General Support** - Help and guidance responses

## 🚀 Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## 📱 Features in Detail

### Chat Interface
- **Auto-scrolling** to newest messages
- **Message persistence** during session
- **Timestamp display** for all messages
- **User/Bot avatars** for clear conversation flow

### Quick Actions
- **Top 5 Products** - Instant access to bestsellers
- **Order Status** - Quick order lookup
- **Stock Check** - Product availability
- **Help Menu** - Available features

### Message Types
- **Text Messages** - Standard chat responses
- **Product Cards** - Rich product displays with pricing
- **Order Information** - Detailed order status with tracking
- **Error Handling** - User-friendly error messages

### Responsive Design
- **Desktop** - Full-width chat interface
- **Tablet** - Optimized layout for medium screens
- **Mobile** - Touch-friendly interface with proper spacing

## 🔌 Backend Integration

To connect with your backend:

1. **Update API Base URL** in `vite.config.js`
2. **Configure CORS** on your backend for `http://localhost:3000`
3. **Implement API endpoints** matching the service layer
4. **Handle authentication** if required

## 🎯 Customization

### Branding
- Update colors in `tailwind.config.js`
- Replace logo in `Header.jsx`
- Modify app title in `index.html`

### Features
- Add new message types in `ChatMessage.jsx`
- Create custom quick actions in `QuickActions.jsx`
- Extend API service in `chatService.js`

## 🐛 Troubleshooting

### Common Issues

1. **Port 3000 already in use:**
   ```bash
   npm run dev -- --port 3001
   ```

2. **API connection errors:**
   - Check backend is running on port 8000
   - Verify CORS configuration
   - Check network tab in browser dev tools

3. **Build failures:**
   ```bash
   # Clear cache and reinstall
   rm -rf node_modules package-lock.json
   npm install
   ```

## 📈 Performance

- **Code Splitting** - Automatic with Vite
- **Lazy Loading** - Components loaded as needed
- **Optimized Images** - Responsive image handling
- **Minimal Bundle** - Tree-shaking eliminates unused code

## 🤝 Contributing

1. Follow the existing code style
2. Use TypeScript for new features (optional)
3. Add proper error handling
4. Test on multiple devices
5. Update documentation

## 📄 License

This project is part of an e-commerce chatbot system. See the main project repository for license information.
