"use client";

import { motion } from "framer-motion";
import { Star } from "lucide-react";
import Image from "next/image";
import Pulse from "../images/Pulse.webp";
import headphone from "../images/headphone.jpg"
import macbook from "../images/apple-macbook.jpg";
import phone from "../images/phone.png";
import USBcable from "../images/USBcable.png"
import Keyboard from "../images/Keyboard.png"
import mouse from "../images/mouse.png"
import webcam from "../images/webcam.png"




const products = [
  {
    name: "Wireless Headphones",
    rating: 4.2,
    reviews: 1234,
    image: headphone,
    trust: 68,
    isImage: true,
  },
  {
    name: "Smart Watch",
    rating: 4.5,
    reviews: 2341,
    image: Pulse,
    trust: 85,
    isImage: true,
  },
  {
    name: "Laptop",
    rating: 3.8,
    reviews: 567,
    image: macbook,
    trust: 45,
    isImage: true,
  },
  {
    name: "Phone",
    rating: 4.7,
    reviews: 3456,
    image: phone,
    trust: 92,
    isImage: true,
  },
  {
    name: "USB Cable",
    rating: 4.1,
    reviews: 890,
    image: USBcable,
    trust: 72,
    isImage: true,
  },
  {
    name: "Keyboard",
    rating: 4.6,
    reviews: 1567,
    image: Keyboard,
    trust: 88,
    isImage: true,
  },
  {
    name: "Mouse",
    rating: 3.9,
    reviews: 432,
    image: mouse,
    trust: 54,
    isImage: true,
  },
  {
    name: "Webcam",
    rating: 4.4,
    reviews: 987,
    image: webcam,
    trust: 78,
    isImage: true,
  },
];

export default function ProductCarousel() {
  return (
    <div className="absolute inset-0 overflow-hidden opacity-30">
      <motion.div
        className="flex space-x-6 py-8"
        animate={{ x: [0, -2000] }}
        transition={{ duration: 40, repeat: Infinity, ease: "linear" }}
      >
        {[...products, ...products, ...products].map((product, index) => (
          <div
            key={index}
            className="flex-shrink-0 w-80 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-4"
          >
            {/* IMAGE / EMOJI */}
            <div className="mb-3 flex justify-center items-center h-64">
              {product.isImage ? (
                <Image
                  src={product.image}
                  alt={product.name}
                  width={64}
                  height={64}
                  className="rounded-lg object-contain"
                />
              ) : (
                <span className="text-6xl">{product.image}</span>
              )}
            </div>

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
