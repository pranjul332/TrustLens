"use client";

import { useAuth0 } from "@auth0/auth0-react";
import { LogIn, LogOut, User } from "lucide-react";
import { motion } from "framer-motion";

export default function AuthButton() {
  const { isAuthenticated, loginWithRedirect, logout, user } = useAuth0();

  if (isAuthenticated) {
    return (
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
            {user?.picture ? (
              <img
                src={user.picture}
                alt={user.name}
                className="w-full h-full rounded-full"
              />
            ) : (
              <User className="w-4 h-4 text-white" />
            )}
          </div>
          <span className="text-white text-sm font-medium">{user?.name}</span>
        </div>
        <button
          onClick={() =>
            logout({ logoutParams: { returnTo: window.location.origin } })
          }
          className="flex items-center space-x-2 px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-all border border-white/10"
        >
          <LogOut className="w-4 h-4" />
          <span>Logout</span>
        </button>
      </div>
    );
  }

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={() => loginWithRedirect()}
      className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-semibold hover:shadow-lg transition-all"
    >
      <LogIn className="w-4 h-4" />
      <span>Sign In</span>
    </motion.button>
  );
}
