import React from 'react'
import { Package, Truck, CheckCircle, Clock, XCircle } from 'lucide-react'
import { format } from 'date-fns'

const OrderInfo = ({ order }) => {
  if (!order) {
    return (
      <div className="bg-red-50 border border-red-200 p-4 rounded-lg max-w-sm">
        <p className="text-red-600">Order not found.</p>
      </div>
    )
  }

  const getStatusIcon = (status) => {
    switch (status.toLowerCase()) {
      case 'pending':
        return <Clock className="h-5 w-5 text-yellow-500" />
      case 'processing':
        return <Package className="h-5 w-5 text-blue-500" />
      case 'shipped':
        return <Truck className="h-5 w-5 text-purple-500" />
      case 'delivered':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'cancelled':
        return <XCircle className="h-5 w-5 text-red-500" />
      default:
        return <Package className="h-5 w-5 text-gray-500" />
    }
  }

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'pending':
        return 'text-yellow-700 bg-yellow-100'
      case 'processing':
        return 'text-blue-700 bg-blue-100'
      case 'shipped':
        return 'text-purple-700 bg-purple-100'
      case 'delivered':
        return 'text-green-700 bg-green-100'
      case 'cancelled':
        return 'text-red-700 bg-red-100'
      default:
        return 'text-gray-700 bg-gray-100'
    }
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 max-w-sm">
      {/* Header */}
      <div className="flex items-center space-x-2 mb-3">
        <Package className="h-5 w-5 text-gray-600" />
        <h3 className="font-semibold text-gray-900">Order #{order.id}</h3>
      </div>

      {/* Order Status */}
      <div className="mb-4">
        <div className="flex items-center space-x-2 mb-2">
          {getStatusIcon(order.status)}
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(order.status)}`}>
            {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
          </span>
        </div>
        
        {order.tracking_number && (
          <p className="text-sm text-gray-600">
            Tracking: <span className="font-mono">{order.tracking_number}</span>
          </p>
        )}
      </div>

      {/* Customer Info */}
      <div className="space-y-2 mb-4">
        <div>
          <p className="text-sm font-medium text-gray-700">Customer</p>
          <p className="text-sm text-gray-600">{order.customer_name}</p>
          {order.customer_email && (
            <p className="text-sm text-gray-600">{order.customer_email}</p>
          )}
        </div>
        
        {order.shipping_address && (
          <div>
            <p className="text-sm font-medium text-gray-700">Shipping Address</p>
            <p className="text-sm text-gray-600">{order.shipping_address}</p>
          </div>
        )}
      </div>

      {/* Order Details */}
      <div className="space-y-2 mb-4">
        <div className="flex justify-between">
          <span className="text-sm text-gray-600">Order Date</span>
          <span className="text-sm font-medium">
            {format(new Date(order.created_at), 'MMM dd, yyyy')}
          </span>
        </div>
        
        {order.total_amount && (
          <div className="flex justify-between">
            <span className="text-sm text-gray-600">Total Amount</span>
            <span className="text-sm font-medium">
              ${parseFloat(order.total_amount).toFixed(2)}
            </span>
          </div>
        )}
      </div>

      {/* Order Items */}
      {order.items && order.items.length > 0 && (
        <div className="border-t pt-3">
          <p className="text-sm font-medium text-gray-700 mb-2">Items ({order.items.length})</p>
          <div className="space-y-2">
            {order.items.map((item, index) => (
              <div key={index} className="flex justify-between text-sm">
                <span className="text-gray-600">
                  {item.product_name} × {item.quantity}
                </span>
                <span className="font-medium">
                  ${parseFloat(item.total_price || item.unit_price * item.quantity).toFixed(2)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="mt-4 pt-3 border-t border-gray-200 space-y-2">
        {order.status === 'shipped' && order.tracking_number && (
          <button className="w-full bg-primary-500 text-white py-2 px-3 rounded-md text-sm font-medium hover:bg-primary-600 transition-colors">
            Track Package
          </button>
        )}
        
        <button className="w-full text-center text-primary-600 hover:text-primary-700 text-sm font-medium">
          View Full Order Details →
        </button>
      </div>
    </div>
  )
}

export default OrderInfo
