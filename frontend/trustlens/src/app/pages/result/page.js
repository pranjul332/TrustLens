"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  ArrowLeft,
  Shield,
  TrendingDown,
  AlertTriangle,
  CheckCircle,
  XCircle,
} from "lucide-react";
import TrustScoreGauge from "@/components/TrustScoreGauge";
import InsightCard from "@/components/InsightCard";
import ScoreBreakdown from "@/components/ScoreBreakdown";
import { analyzeProduct } from "@/lib/api";
import { useAuth0 } from "@auth0/auth0-react";
import LoadingSpinner from "@/components/LoadingSpinner";

export default function AnalyzePage() {
  const router = useRouter();
  const { getAccessTokenSilently, isAuthenticated } = useAuth0();

  const [loading, setLoading] = useState(true);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [productUrl, setProductUrl] = useState("");

  useEffect(() => {
    const analyzeURL = async () => {
      if (!isAuthenticated) {
        router.push("/");
        return;
      }

      const url = sessionStorage.getItem("productUrl");
      if (!url) {
        router.push("/");
        return;
      }

      setProductUrl(url);

      try {
        const token = await getAccessTokenSilently();
        const data = await analyzeProduct(url, token);
        setResult(data);
      } catch (err) {
        setError(err?.message || "Failed to analyze product");
      } finally {
        setLoading(false);
      }
    };

    analyzeURL();
  }, [isAuthenticated, getAccessTokenSilently, router]);

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case "low":
        return "text-green-400";
      case "medium":
        return "text-yellow-400";
      case "high":
        return "text-orange-400";
      case "critical":
        return "text-red-400";
      default:
        return "text-gray-400";
    }
  };

  const getRiskIcon = (riskLevel) => {
    switch (riskLevel) {
      case "low":
        return CheckCircle;
      case "medium":
        return AlertTriangle;
      case "high":
        return TrendingDown;
      case "critical":
        return XCircle;
      default:
        return AlertTriangle;
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
        <div className="bg-red-500/10 border border-red-500/50 rounded-2xl p-8 max-w-md text-center">
          <XCircle className="w-16 h-16 text-red-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-white mb-2">
            Analysis Failed
          </h2>
          <p className="text-gray-300 mb-6">{error}</p>
          <button
            onClick={() => router.push("/")}
            className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-semibold hover:shadow-lg transition-all"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!result) return null;

  const RiskIcon = getRiskIcon(result.risk_level);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute top-20 right-20 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-10"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.1, 0.15, 0.1],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      </div>

      {/* Header */}
      <header className="relative z-10 border-b border-white/10 backdrop-blur-lg bg-white/5">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <button
            onClick={() => router.push("/")}
            className="flex items-center space-x-2 text-gray-300 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back to Home</span>
          </button>
        </div>
      </header>

      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Product URL */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-4">
            <p className="text-gray-400 text-sm mb-1">Analyzing Product</p>
            <p className="text-white font-medium truncate">{productUrl}</p>
          </div>
        </motion.div>

        {/* Main Score Section */}
        <div className="grid lg:grid-cols-2 gap-8 mb-12">
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <TrustScoreGauge
              score={result.trust_score}
              riskLevel={result.risk_level}
              confidence={result.confidence}
            />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="space-y-4"
          >
            <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-white font-semibold">Risk Assessment</h3>
                <RiskIcon
                  className={`w-6 h-6 ${getRiskColor(result.risk_level)}`}
                />
              </div>

              <div className="space-y-3">
                <div>
                  <p className="text-gray-400 text-sm mb-1">Risk Level</p>
                  <p
                    className={`text-2xl font-bold uppercase ${getRiskColor(
                      result.risk_level,
                    )}`}
                  >
                    {result.risk_level}
                  </p>
                </div>

                <div>
                  <p className="text-gray-400 text-sm mb-1">Fake Reviews</p>
                  <p className="text-white text-xl font-semibold">
                    {result.fake_reviews_percentage.toFixed(1)}%
                  </p>
                </div>

                <div>
                  <p className="text-gray-400 text-sm mb-1">Reviews Analyzed</p>
                  <p className="text-white text-lg">
                    {result.total_reviews_analyzed}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-purple-500/10 to-pink-500/10 border border-purple-500/30 rounded-2xl p-6">
              <div className="flex items-start space-x-3">
                <Shield className="w-6 h-6 text-purple-400 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="text-white font-semibold mb-2">
                    Our Recommendation
                  </h3>
                  <p className="text-gray-300">{result.recommendation}</p>
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-12"
        >
          <ScoreBreakdown breakdown={result.score_breakdown} />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <h2 className="text-2xl font-bold text-white mb-6">
            Detailed Insights
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {result.key_insights.map((insight, index) => (
              <InsightCard
                key={index}
                insight={insight}
                delay={0.6 + index * 0.1}
              />
            ))}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="mt-12 text-center text-gray-400 text-sm"
        >
          <p>
            Analysis completed on {new Date(result.timestamp).toLocaleString()}
          </p>
          <p className="mt-1">Report valid for 7 days</p>
        </motion.div>
      </main>
    </div>
  );
}
