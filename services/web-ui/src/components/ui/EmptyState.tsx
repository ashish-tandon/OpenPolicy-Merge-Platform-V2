import React from "react";

export const EmptyState: React.FC<{ title: string; description: string; icon?: React.ReactNode }> = ({ title, description, icon }) => (
  <div className="text-center py-12">
    {icon && <div className="mx-auto h-12 w-12 text-gray-400 mb-4">{icon}</div>}
    <h3 className="text-sm font-medium text-gray-900">{title}</h3>
    <p className="mt-1 text-sm text-gray-500">{description}</p>
  </div>
);

export const LoadingState: React.FC<{ message?: string }> = ({ message = "Loading..." }) => (
  <div className="text-center py-12">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
    <p className="text-sm text-gray-500">{message}</p>
  </div>
);
