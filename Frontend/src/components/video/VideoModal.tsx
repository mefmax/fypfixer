import React, { useEffect } from 'react';
import { useUIStore } from '../../store/uiStore';

export const VideoModal: React.FC = () => {
  const { isVideoModalOpen, currentVideo, closeVideoModal } = useUIStore();

  // Close on Escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') closeVideoModal();
    };

    if (isVideoModalOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isVideoModalOpen, closeVideoModal]);

  if (!isVideoModalOpen || !currentVideo) return null;

  const handleOpenInTikTok = () => {
    window.open(currentVideo.video_url, '_blank');
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm"
      onClick={closeVideoModal}
    >
      <div
        className="relative w-full max-w-md h-[90vh] max-h-[800px] bg-black rounded-xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close button */}
        <button
          className="absolute top-4 right-4 z-10 w-10 h-10 rounded-full bg-black/70 text-white flex items-center justify-center hover:bg-black/90 transition-colors"
          onClick={closeVideoModal}
        >
          ✕
        </button>

        {/* Video embed placeholder */}
        <div className="w-full h-full flex flex-col">
          {/* TikTok Embed */}
          <div className="flex-1 bg-gray-900 flex items-center justify-center">
            <iframe
              src={`https://www.tiktok.com/embed/v2/${currentVideo.video_id}`}
              className="w-full h-full border-none"
              allowFullScreen
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            />
          </div>

          {/* Bottom actions */}
          <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/90 to-transparent">
            <div className="mb-3">
              <h3 className="text-white font-semibold line-clamp-1">
                {currentVideo.title}
              </h3>
              <p className="text-gray-400 text-sm">
                {currentVideo.creator_username}
              </p>
            </div>

            <button
              onClick={handleOpenInTikTok}
              className="w-full py-3 rounded-xl bg-gradient-to-r from-primary to-secondary text-white font-semibold hover:opacity-90 transition-opacity"
            >
              🎬 Open in TikTok
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
