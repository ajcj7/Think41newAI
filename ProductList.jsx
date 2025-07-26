import React from 'react'
import { ShoppingCart, Star, Package } from 'lucide-react'

const ProductList = ({ products }) => {
  if (!products || products.length === 0) {
    return (
      <div className="bg-gray-100 p-4 rounded-lg">
        <p className="text-gray-600">No products found.</p>
      </div>
    )
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 max-w-sm">
      <div className="flex items-center space-x-2 mb-3">
        <Star className="h-5 w-5 text-yellow-500" />
        <h3 className="font-semibold text-gray-900">Top Products</h3>
      </div>
      
      <div className="space-y-3">
        {products.map((product, index) => (
          <div key={product.id || index} className="flex items-center space-x-3 p-2 hover:bg-gray-50 rounded-lg transition-colors">
            {/* Rank */}
            <div className="flex-shrink-0 w-6 h-6 bg-primary-500 text-white text-xs font-bold rounded-full flex items-center justify-center">
              {index + 1}
            </div>
            
            {/* Product Info */}
            <div className="flex-1 min-w-0">
              <p className="font-medium text-gray-900 truncate">
                {product.name}
              </p>
              <div className="flex items-center space-x-4 text-xs text-gray-500">
                <span className="flex items-center space-x-1">
                  <ShoppingCart className="h-3 w-3" />
                  <span>{product.total_sold} sold</span>
                </span>
                <span className="flex items-center space-x-1">
                  <Package className="h-3 w-3" />
                  <span>{product.stock_quantity} in stock</span>
                </span>
              </div>
            </div>
            
            {/* Price */}
            <div className="flex-shrink-0 text-right">
              <p className="font-semibold text-gray-900">
                ${parseFloat(product.price).toFixed(2)}
              </p>
              {product.category && (
                <p className="text-xs text-gray-500">
                  {product.category}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-3 pt-3 border-t border-gray-200">
        <button className="w-full text-center text-primary-600 hover:text-primary-700 text-sm font-medium">
          View All Products →
        </button>
      </div>
    </div>
  )
}

export default ProductList
