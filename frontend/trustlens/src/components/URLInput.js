"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Search, Loader2, AlertCircle, Globe } from "lucide-react";
import { validateProductUrl } from "@/lib/api";

export default function URLInput({ onAnalyze, loading }) {
  const [url, setUrl] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    if (!url.trim()) {
      setError("Please enter a product URL");
      return;
    }

    // Validate URL
    const validation = validateProductUrl(url);
    if (!validation.valid) {
      setError(validation.error);
      return;
    }

    // Call the analysis function
    onAnalyze(url);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4 }}
      className="max-w-3xl mx-auto"
    >
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative group">
          <input
            type="text"
            value={url}
            onChange={(e) => {
              setUrl(e.target.value);
              setError(""); // Clear error on input
            }}
            placeholder="Paste any product URL from any e-commerce site"
            disabled={loading}
            className={`w-full px-6 py-5 pr-40 rounded-2xl bg-white/10 backdrop-blur-md border-2 ${
              error
                ? "border-red-500/50 focus:border-red-500"
                : "border-white/20 focus:border-purple-500"
            } text-white placeholder-gray-400 focus:outline-none transition-all text-lg ${
              loading ? "opacity-50 cursor-not-allowed" : ""
            }`}
          />
          <button
            type="submit"
            disabled={loading}
            className={`absolute right-2 top-1/2 -translate-y-1/2 px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl font-semibold hover:shadow-lg hover:shadow-purple-500/50 transition-all flex items-center space-x-2 ${
              loading ? "opacity-50 cursor-not-allowed" : ""
            }`}
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Search className="w-5 h-5" />
                <span>Analyze</span>
              </>
            )}
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-3 flex items-center space-x-2 text-red-400 text-sm"
          >
            <AlertCircle className="w-4 h-4" />
            <span>{error}</span>
          </motion.div>
        )}

        {/* Supported Platforms Info */}
        <div className="mt-4 flex items-center justify-center space-x-4 text-sm text-gray-400">
          <Globe className="w-4 h-4" />
          <span>
            Works with Amazon, Flipkart, Myntra, Walmart, eBay, and more
          </span>
        </div>
      </form>
    </motion.div>
  );
}
