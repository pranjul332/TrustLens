"use client";

import { motion } from "framer-motion";

export default function FeatureCard({
  icon: Icon,
  title,
  description,
  color,
  delay,
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      whileHover={{ y: -5 }}
      className="relative group"
    >
      <div
        className="absolute -inset-0.5 bg-gradient-to-r opacity-20 group-hover:opacity-40 rounded-2xl blur transition-opacity"
        style={{
          backgroundImage: `linear-gradient(to right, var(--tw-gradient-stops))`,
        }}
      />
      <div className="relative bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 h-full hover:bg-white/10 transition-all">
        <div
          className={`w-14 h-14 mb-6 rounded-xl bg-gradient-to-br ${color} flex items-center justify-center`}
        >
          <Icon className="w-7 h-7 text-white" />
        </div>
        <h3 className="text-xl font-bold text-white mb-3">{title}</h3>
        <p className="text-gray-400 leading-relaxed">{description}</p>
      </div>
    </motion.div>
  );
}
