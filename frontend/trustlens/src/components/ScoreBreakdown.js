"use client";

import { motion } from "framer-motion";
import { Brain, Activity, BarChart3 } from "lucide-react";

export default function ScoreBreakdown({ breakdown }) {
  // Add safety check and logging
  console.log("ScoreBreakdown received:", breakdown);

  // Safely extract values with defaults
  const safeValue = (value) => {
    const num = typeof value === "number" ? value : 0;
    return isNaN(num) ? 0 : num;
  };

  const components = [
    {
      name: "NLP Analysis",
      value: safeValue(breakdown?.nlp_contribution),
      icon: Brain,
      color: "from-purple-500 to-pink-500",
      description: "Text and sentiment analysis",
    },
    {
      name: "Behavioral Patterns",
      value: safeValue(breakdown?.behavior_contribution),
      icon: Activity,
      color: "from-blue-500 to-cyan-500",
      description: "Temporal and reviewer patterns",
    },
    {
      name: "Statistical Analysis",
      value: safeValue(breakdown?.statistical_contribution),
      icon: BarChart3,
      color: "from-orange-500 to-red-500",
      description: "Rating distribution analysis",
    },
  ];

  return (
    <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8">
      <h2 className="text-2xl font-bold text-white mb-6">Score Breakdown</h2>

      <div className="grid md:grid-cols-3 gap-6">
        {components.map((component, index) => {
          const Icon = component.icon;

          return (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 * index }}
              className="bg-white/5 border border-white/10 rounded-xl p-6"
            >
              <div className="flex items-center justify-between mb-4">
                <div
                  className={`w-12 h-12 rounded-lg bg-gradient-to-br ${component.color} flex items-center justify-center`}
                >
                  <Icon className="w-6 h-6 text-white" />
                </div>

                <div className="text-right">
                  <div className="text-2xl font-bold text-white">
                    {component.value.toFixed(1)}
                  </div>
                  <div className="text-xs text-gray-400">points</div>
                </div>
              </div>

              <h3 className="text-white font-semibold mb-1">
                {component.name}
              </h3>
              <p className="text-gray-400 text-sm">{component.description}</p>

              <div className="mt-4">
                <div className="w-full bg-white/10 rounded-full h-2">
                  <motion.div
                    className={`bg-gradient-to-r ${component.color} h-2 rounded-full`}
                    initial={{ width: 0 }}
                    animate={{
                      width: `${Math.min((component.value / 50) * 100, 100)}%`,
                    }}
                    transition={{
                      delay: 0.5 + 0.1 * index,
                      duration: 1,
                    }}
                  />
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
