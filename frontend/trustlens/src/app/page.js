"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Shield, Search, TrendingUp, AlertCircle } from "lucide-react";
import ProductCarousel from "@/components/ProductCarousel";
import URLInput from "@/components/URLInput";
import FeatureCard from "@/components/FeatureCard";
import { useAuth0 } from "@auth0/auth0-react";
import AuthButton from "@/components/AuthButton";

export default function HomePage() {
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const { isAuthenticated, loginWithRedirect } = useAuth0();

  const handleAnalyze = async (url) => {
    if (!isAuthenticated) {
      loginWithRedirect();
      return;
    }

    setLoading(true);
    // Store URL in sessionStorage and navigate
    sessionStorage.setItem("productUrl", url);
    router.push("/analyze");
  };

  const features = [
    {
      icon: Shield,
      title: "AI-Powered Detection",
      description:
        "Advanced NLP algorithms detect fake reviews with 90%+ accuracy",
      color: "from-blue-500 to-cyan-500",
    },
    {
      icon: TrendingUp,
      title: "Behavioral Analysis",
      description:
        "Identifies suspicious patterns in review timing and distribution",
      color: "from-purple-500 to-pink-500",
    },
    {
      icon: AlertCircle,
      title: "Real-Time Reports",
      description:
        "Get instant trust scores and detailed insights on any product",
      color: "from-orange-500 to-red-500",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
      {/* Animated background gradient orbs */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20"
          animate={{ x: [0, 100, 0], y: [0, 50, 0] }}
          transition={{ duration: 20, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="absolute -bottom-40 -left-40 w-80 h-80 bg-cyan-500 rounded-full mix-blend-multiply filter blur-xl opacity-20"
          animate={{ x: [0, -100, 0], y: [0, -50, 0] }}
          transition={{ duration: 25, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="absolute top-1/2 left-1/2 w-80 h-80 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-20"
          animate={{ x: [0, 50, 0], y: [0, -100, 0] }}
          transition={{ duration: 30, repeat: Infinity, ease: "easeInOut" }}
        />
      </div>

      

      {/* Header */}
      <header className="relative z-10 border-b border-white/10 backdrop-blur-lg bg-white/5">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center space-x-3"
            >
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold text-white">TrustScore</span>
            </motion.div>

            <AuthButton />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="inline-block mb-4"
          >
            <span className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-purple-500/20 text-purple-300 border border-purple-500/30">
              <Search className="w-4 h-4 mr-2" />
              AI-Powered Review Analysis
            </span>
          </motion.div>
{/* Product Carousel Background */}
      <ProductCarousel />
          <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-6 leading-tight">
            Don't Get Fooled by
            <span className="block bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400 text-transparent bg-clip-text">
              Fake Reviews
            </span>
          </h1>

          <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-3xl mx-auto">
            Uncover the truth behind product reviews with our advanced AI
            analysis. Make informed decisions with confidence.
          </p>

          {/* URL Input */}
          <URLInput onAnalyze={handleAnalyze} loading={loading} />

          {/* Trusted by badge */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1 }}
            className="mt-8 flex items-center justify-center space-x-8 text-gray-400 text-sm"
          >
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span>10,000+ Products Analyzed</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
              <span>90%+ Accuracy Rate</span>
            </div>
          </motion.div>
        </motion.div>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.8 }}
          className="grid md:grid-cols-3 gap-8 mb-20"
        >
          {features.map((feature, index) => (
            <FeatureCard key={index} {...feature} delay={0.6 + index * 0.1} />
          ))}
        </motion.div>

        {/* How It Works */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="text-center"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-12">
            How It Works
          </h2>

          <div className="grid md:grid-cols-4 gap-8">
            {[
              {
                step: "1",
                title: "Paste URL",
                desc: "Copy product link from Amazon, Flipkart, or Myntra",
              },
              {
                step: "2",
                title: "AI Analysis",
                desc: "Our AI analyzes reviews, patterns, and behaviors",
              },
              {
                step: "3",
                title: "Get Score",
                desc: "Receive trust score and detailed insights",
              },
              {
                step: "4",
                title: "Decide",
                desc: "Make informed purchase decisions",
              },
            ].map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1 + index * 0.1 }}
                className="relative"
              >
                <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6 hover:bg-white/10 transition-all">
                  <div className="w-12 h-12 mx-auto mb-4 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white font-bold text-xl">
                    {item.step}
                  </div>
                  <h3 className="text-white font-semibold mb-2">
                    {item.title}
                  </h3>
                  <p className="text-gray-400 text-sm">{item.desc}</p>
                </div>
                {index < 3 && (
                  <div className="hidden md:block absolute top-1/2 -right-4 w-8 h-0.5 bg-gradient-to-r from-purple-500 to-transparent" />
                )}
              </motion.div>
            ))}
          </div>
        </motion.div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/10 backdrop-blur-lg bg-white/5 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-400 text-sm">
            <p>© 2026 TrustScore. Powered by Advanced AI & Machine Learning.</p>
            <p className="mt-2">
              Helping millions make smarter purchase decisions.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
