import React from "react";

export default function LoadingSpinner({ size = 48, message = "Loading...", fullScreen = true }) {
  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8 shadow-2xl flex flex-col items-center">
          <div
            style={{ width: size, height: size }}
            className="rounded-full animate-spin border-4 border-indigo-200 border-t-indigo-600 mb-4"
          />
          <p className="text-gray-700 font-semibold text-lg">{message}</p>
        </div>
      </div>
    );
  }

  // Inline spinner for non-full-screen usage
  return (
    <div className="flex flex-col items-center justify-center py-4">
      <div
        style={{ width: size, height: size }}
        className="rounded-full animate-spin border-4 border-indigo-200 border-t-indigo-600"
      />
      {message && <p className="mt-3 text-gray-600">{message}</p>}
    </div>
  );
}
