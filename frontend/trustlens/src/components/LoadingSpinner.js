"use client";

import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";

export default function LoadingSpinner() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        className="text-center"
      >
        <Loader2 className="w-16 h-16 text-purple-400 animate-spin mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-white mb-2">
          Analyzing Reviews...
        </h2>
        <p className="text-gray-400">This may take a few moments</p>

        <div className="mt-8 space-y-2">
          {[
            "Extracting reviews",
            "Running NLP analysis",
            "Detecting patterns",
            "Calculating trust score",
          ].map((text, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.3 }}
              className="text-gray-500 text-sm"
            >
              {text}...
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
