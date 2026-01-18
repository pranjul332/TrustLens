"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
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
import LoadingSpinner from "@/components/LoadingSpinner";

export default function AnalyzePage() {
  const router = useRouter();
  const hasAnalyzed = useRef(false);

  const [loading, setLoading] = useState(true);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [productUrl, setProductUrl] = useState("");

  const safeNumber = (value, defaultValue = 0) => {
    const num = typeof value === "number" ? value : defaultValue;
    return isNaN(num) ? defaultValue : num;
  };

  useEffect(() => {
    if (hasAnalyzed.current) return;
    hasAnalyzed.current = true;

    const runAnalysis = async () => {
      const url = sessionStorage.getItem("productUrl");

      if (!url) {
        router.push("/");
        return;
      }

      setProductUrl(url);

      try {
        const data = await analyzeProduct(url);

        console.log("Raw API response:", data); // Debug log

        if (!data || typeof data !== "object") {
          throw new Error("Invalid response from server");
        }

        const sanitizedData = {
          trust_score: safeNumber(data.trust_score),
          risk_level: data.risk_level || "medium",
          confidence: safeNumber(data.confidence),
          fake_reviews_percentage: safeNumber(data.fake_reviews_percentage),
          total_reviews_analyzed: safeNumber(data.total_reviews_analyzed),
          recommendation:
            data.recommendation || "Unable to generate recommendation",
          score_breakdown: {
            nlp_contribution: safeNumber(
              data.score_breakdown?.nlp_contribution,
            ),
            behavior_contribution: safeNumber(
              data.score_breakdown?.behavior_contribution,
            ),
            statistical_contribution: safeNumber(
              data.score_breakdown?.statistical_contribution,
            ),
            final_score: safeNumber(data.score_breakdown?.final_score),
          },
          key_insights: Array.isArray(data.key_insights)
            ? data.key_insights
            : [],
        };

        console.log("Sanitized data:", sanitizedData); // Debug log
        setResult(sanitizedData);
      } catch (err) {
        console.error("Analysis error:", err);
        setError(err?.message || "Failed to analyze product");
      } finally {
        setLoading(false);
      }
    };

    runAnalysis();
  }, [router]);

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
            className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-semibold"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!result) return null;

  const getRiskColor = (risk) => {
    switch (risk?.toLowerCase()) {
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

  const getRiskIcon = (risk) => {
    switch (risk?.toLowerCase()) {
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

  const RiskIcon = getRiskIcon(result.risk_level);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <header className="border-b border-white/10 bg-white/5">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <button
            onClick={() => router.push("/")}
            className="flex items-center space-x-2 text-gray-300 hover:text-white"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back</span>
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-12">
        <div className="mb-8 bg-white/5 border border-white/10 rounded-xl p-4">
          <p className="text-gray-400 text-sm">Analyzed Product</p>
          <p className="text-white truncate">{productUrl}</p>
        </div>

        {/* Stats Overview */}
        <div className="mb-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white/5 border border-white/10 rounded-xl p-4">
            <p className="text-gray-400 text-sm">Fake Reviews</p>
            <p className="text-2xl font-bold text-red-400">
              {result.fake_reviews_percentage.toFixed(1)}%
            </p>
          </div>
          {/* <div className="bg-white/5 border border-white/10 rounded-xl p-4">
            <p className="text-gray-400 text-sm">Reviews Analyzed</p>
            <p className="text-2xl font-bold text-white">
              {result.total_reviews_analyzed}
            </p>
          </div> */}
          {/* <div className="bg-white/5 border border-white/10 rounded-xl p-4">
            <p className="text-gray-400 text-sm">Analysis Confidence</p>
            <p className="text-2xl font-bold text-purple-400">
              {(result.confidence * 100).toFixed(0)}%
            </p>
          </div> */}
        </div>

        <div className="grid lg:grid-cols-2 gap-8 mb-12">
          <TrustScoreGauge
            score={result.trust_score}
            riskLevel={result.risk_level}
            confidence={result.confidence}
          />

          <div className="space-y-4">
            <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
              <h3 className="text-white font-semibold mb-3">Risk Level</h3>
              <div className="flex items-center gap-3">
                <RiskIcon
                  className={`w-6 h-6 ${getRiskColor(result.risk_level)}`}
                />
                <span
                  className={`text-2xl font-bold uppercase ${getRiskColor(result.risk_level)}`}
                >
                  {result.risk_level}
                </span>
              </div>
            </div>

            <div className="bg-purple-500/10 border border-purple-500/30 rounded-2xl p-6">
              <Shield className="w-6 h-6 text-purple-400 mb-2" />
              <p className="text-gray-300">{result.recommendation}</p>
            </div>
          </div>
        </div>

        {result.score_breakdown && (
          <ScoreBreakdown breakdown={result.score_breakdown} />
        )}

        {result.key_insights && result.key_insights.length > 0 && (
          <div className="mt-12">
            <h2 className="text-2xl font-bold text-white mb-6">Key Insights</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {result.key_insights.map((insight, index) => (
                <InsightCard
                  key={index}
                  insight={insight}
                  delay={index * 0.1}
                />
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
