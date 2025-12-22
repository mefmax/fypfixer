import React, { useEffect } from 'react';
import { AlertCircle, CheckCircle, X } from 'lucide-react';
import { clsx } from 'clsx';

interface ToastProps {
  message: string;
  type: 'error' | 'success';
  onClose: () => void;
}

export const Toast: React.FC<ToastProps> = ({ message, type, onClose }) => {
  useEffect(() => {
    const timer = setTimeout(onClose, 5000); // Auto-close after 5s
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div
      className={clsx(
        'fixed bottom-4 right-4 z-50',
        'flex items-center gap-3 px-4 py-3 rounded-xl',
        'backdrop-blur-sm shadow-lg animate-in slide-in-from-bottom-4',
        type === 'error'
          ? 'bg-red-500/20 border border-red-500/50'
          : 'bg-green-500/20 border border-green-500/50'
      )}
    >
      {type === 'error' ? (
        <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
      ) : (
        <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0" />
      )}
      <p className="text-white text-sm">{message}</p>
      <button
        onClick={onClose}
        className="text-white/60 hover:text-white ml-2 flex-shrink-0"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  );
};
