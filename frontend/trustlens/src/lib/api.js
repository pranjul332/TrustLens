/**
 * API utility functions for connecting to the backend
 */

// Backend API base URL - update this based on your deployment
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Analyze a product by URL
 * @param {string} productUrl - The product URL to analyze
 * @param {boolean} forceRefresh - Whether to force a fresh analysis (bypass cache)
 * @returns {Promise<Object>} Analysis results
 */
export async function analyzeProduct(productUrl, forceRefresh = false) {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        product_url: productUrl,
        force_refresh: forceRefresh,
      }),
    });

    // Handle rate limiting
    if (response.status === 429) {
      const errorData = await response.json();
      throw new Error(
        errorData.detail || "Too many requests. Please try again later.",
      );
    }

    // Handle other errors
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `Analysis failed with status: ${response.status}`,
      );
    }

    const data = await response.json();
    return data;
  } catch (error) {
    // Network errors or other issues
    if (error.message.includes("fetch")) {
      throw new Error(
        "Unable to connect to analysis server. Please check your connection.",
      );
    }
    throw error;
  }
}

/**
 * Check backend health status
 * @returns {Promise<Object>} Health status
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error("Health check failed");
    }
    return await response.json();
  } catch (error) {
    console.error("Health check error:", error);
    return { status: "unhealthy", error: error.message };
  }
}

/**
 * Validate a product URL before analysis
 * @param {string} url - URL to validate
 * @returns {Object} Validation result
 */
export function validateProductUrl(url) {
  try {
    const urlObj = new URL(url);
    const hostname = urlObj.hostname.toLowerCase();

    // Common e-commerce platforms (for display purposes)
    const knownPlatforms = [
      {
        name: "Amazon",
        domains: [
          "amazon.in",
          "amazon.com",
          "amazon.co.uk",
          "amazon.de",
          "amazon.fr",
        ],
      },
      { name: "Flipkart", domains: ["flipkart.com"] },
      { name: "Myntra", domains: ["myntra.com"] },
      { name: "Walmart", domains: ["walmart.com"] },
      { name: "eBay", domains: ["ebay.com", "ebay.in", "ebay.co.uk"] },
      { name: "AliExpress", domains: ["aliexpress.com"] },
      { name: "Etsy", domains: ["etsy.com"] },
      { name: "Target", domains: ["target.com"] },
      { name: "Best Buy", domains: ["bestbuy.com"] },
    ];

    // Find platform if it matches known ones
    let platformName = "Other";
    for (const platform of knownPlatforms) {
      if (platform.domains.some((domain) => hostname.includes(domain))) {
        platformName = platform.name;
        break;
      }
    }

    // Accept any valid URL
    return {
      valid: true,
      platform: platformName,
      url: url,
    };
  } catch (error) {
    return {
      valid: false,
      error: "Invalid URL format. Please enter a valid product URL.",
    };
  }
}

export default {
  analyzeProduct,
  checkHealth,
  validateProductUrl,
};
