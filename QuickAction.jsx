
import React from 'react'

const QuickActions = ({ actions, onActionClick }) => {
  return (
    <div className="border-b bg-gray-50 p-4">
      <h4 className="text-sm font-medium text-gray-700 mb-3">
        Quick Actions - Click to get started:
      </h4>
      
      <div className="grid grid-cols-2 gap-2">
        {actions.map((action) => (
          <button
            key={action.id}
            onClick={() => onActionClick(action)}
            className="flex items-center space-x-3 p-3 bg-white border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-all duration-200 text-left group"
          >
            <span className="text-xl group-hover:scale-110 transition-transform">
              {action.icon}
            </span>
            <div>
              <div className="font-medium text-gray-900 text-sm">
                {action.label}
              </div>
              <div className="text-xs text-gray-500 mt-1">
                {action.message}
              </div>
            </div>
          </button>
        ))}
      </div>

      <div className="mt-4 text-center">
        <p className="text-xs text-gray-500">
          Or type your question in the message box below
        </p>
      </div>
    </div>
  )
}

export default QuickActions
