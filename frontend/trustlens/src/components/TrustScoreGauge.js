"use client";

import { motion } from "framer-motion";
import { Shield } from "lucide-react";

export default function TrustScoreGauge({ score, riskLevel, confidence }) {
  const getColor = (score) => {
    if (score >= 80) return "from-green-500 to-emerald-500";
    if (score >= 60) return "from-yellow-500 to-orange-500";
    if (score >= 40) return "from-orange-500 to-red-500";
    return "from-red-500 to-rose-500";
  };

  const circumference = 2 * Math.PI * 80;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8">
      <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
        <Shield className="w-6 h-6 mr-2" />
        Trust Score
      </h2>

      <div className="relative w-64 h-64 mx-auto">
        <svg className="w-full h-full transform -rotate-90">
          {/* Background circle */}
          <circle
            cx="128"
            cy="128"
            r="80"
            stroke="rgba(255,255,255,0.1)"
            strokeWidth="20"
            fill="none"
          />

          {/* Progress circle */}
          <motion.circle
            cx="128"
            cy="128"
            r="80"
            stroke="url(#gradient)"
            strokeWidth="20"
            fill="none"
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset }}
            transition={{ duration: 2, ease: "easeOut" }}
          />

          <defs>
            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop
                offset="0%"
                className={`text-${getColor(score).split("-")[1]}-500`}
                stopColor="currentColor"
              />
              <stop
                offset="100%"
                className={`text-${getColor(score).split("-")[3]}-500`}
                stopColor="currentColor"
              />
            </linearGradient>
          </defs>
        </svg>

        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.5, type: "spring" }}
            className="text-center"
          >
            <div
              className={`text-6xl font-bold bg-gradient-to-br ${getColor(
                score,
              )} text-transparent bg-clip-text`}
            >
              {score}
            </div>
            <div className="text-gray-400 text-sm mt-1">out of 100</div>
          </motion.div>
        </div>
      </div>

      <div className="mt-6 pt-6 border-t border-white/10">
        <div className="flex items-center justify-between mb-2">
          <span className="text-gray-400">Confidence</span>
          <span className="text-white font-semibold">
            {(confidence * 100).toFixed(0)}%
          </span>
        </div>
        <div className="w-full bg-white/10 rounded-full h-2">
          <motion.div
            className="bg-gradient-to-r from-blue-500 to-cyan-500 h-2 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${confidence * 100}%` }}
            transition={{ delay: 1, duration: 1 }}
          />
        </div>
      </div>
    </div>
  );
}
