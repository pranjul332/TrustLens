"use client";

import { motion } from "framer-motion";
import { AlertTriangle, AlertCircle, CheckCircle } from "lucide-react";

export default function InsightCard({ insight, delay }) {
  const getIcon = () => {
    if (insight.category === "red_flag") return AlertTriangle;
    if (insight.category === "warning") return AlertCircle;
    return CheckCircle;
  };

  const getColor = () => {
    if (insight.severity === "high") return "from-red-500 to-rose-500";
    if (insight.severity === "medium") return "from-yellow-500 to-orange-500";
    return "from-green-500 to-emerald-500";
  };

  const getBgColor = () => {
    if (insight.severity === "high") return "bg-red-500/10 border-red-500/30";
    if (insight.severity === "medium")
      return "bg-yellow-500/10 border-yellow-500/30";
    return "bg-green-500/10 border-green-500/30";
  };

  const Icon = getIcon();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className={`${getBgColor()} backdrop-blur-sm border rounded-xl p-6 hover:scale-105 transition-transform`}
    >
      <div className="flex items-start space-x-3 mb-3">
        <div
          className={`w-10 h-10 rounded-lg bg-gradient-to-br ${getColor()} flex items-center justify-center flex-shrink-0`}
        >
          <Icon className="w-5 h-5 text-white" />
        </div>
        <div className="flex-1">
          <h3 className="text-white font-semibold mb-1">{insight.title}</h3>
          <span className="text-xs uppercase font-semibold text-gray-400">
            {insight.severity} severity
          </span>
        </div>
      </div>

      <p className="text-gray-300 text-sm mb-2">{insight.description}</p>

      {insight.evidence && (
        <p className="text-gray-500 text-xs italic">{insight.evidence}</p>
      )}
    </motion.div>
  );
}
