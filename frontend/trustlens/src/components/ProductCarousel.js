"use client";

import { motion } from "framer-motion";
import { Star } from "lucide-react";

const products = [
  {
    name: "Wireless Headphones",
    rating: 4.2,
    reviews: 1234,
    image: "🎧",
    trust: 68,
  },
  { name: "Smart Watch", rating: 4.5, reviews: 2341, image: "⌚", trust: 85 },
  { name: "Laptop Stand", rating: 3.8, reviews: 567, image: "💻", trust: 45 },
  { name: "Phone Case", rating: 4.7, reviews: 3456, image: "📱", trust: 92 },
  { name: "USB Cable", rating: 4.1, reviews: 890, image: "🔌", trust: 72 },
  { name: "Keyboard", rating: 4.6, reviews: 1567, image: "⌨️", trust: 88 },
  { name: "Mouse Pad", rating: 3.9, reviews: 432, image: "🖱️", trust: 54 },
  { name: "Webcam", rating: 4.4, reviews: 987, image: "📷", trust: 78 },
];

export default function ProductCarousel() {
  return (
    <div className="absolute inset-0 overflow-hidden opacity-20">
      <motion.div
        className="flex space-x-6 py-8"
        animate={{
          x: [0, -2000],
        }}
        transition={{
          duration: 40,
          repeat: Infinity,
          ease: "linear",
        }}
      >
        {[...products, ...products, ...products].map((product, index) => (
          <div
            key={index}
            className="flex-shrink-0 w-64 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-4"
          >
            <div className="text-6xl mb-3 text-center">{product.image}</div>
            <h3 className="text-white font-semibold text-sm mb-2 truncate">
              {product.name}
            </h3>
            <div className="flex items-center justify-between text-xs">
              <div className="flex items-center space-x-1">
                <Star className="w-3 h-3 fill-yellow-400 text-yellow-400" />
                <span className="text-gray-300">{product.rating}</span>
                <span className="text-gray-500">({product.reviews})</span>
              </div>
              <div
                className={`px-2 py-1 rounded ${
                  product.trust > 80
                    ? "bg-green-500/20 text-green-400"
                    : product.trust > 60
                      ? "bg-yellow-500/20 text-yellow-400"
                      : "bg-red-500/20 text-red-400"
                }`}
              >
                {product.trust}%
              </div>
            </div>
          </div>
        ))}
      </motion.div>
    </div>
  );
}
