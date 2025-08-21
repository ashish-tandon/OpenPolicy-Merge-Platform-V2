'use client';

import { ReactNode, useState, useRef, useEffect } from 'react';
import { 
  PlayIcon, 
  PauseIcon, 
  SpeakerWaveIcon, 
  SpeakerXMarkIcon,
  ArrowsPointingOutIcon,
  ArrowsPointingInIcon,
  ForwardIcon,
  BackwardIcon
} from '@heroicons/react/24/outline';

// Utility function for combining class names
const cn = (...classes: (string | undefined | null | false)[]) => {
  return classes.filter(Boolean).join(' ');
};

// Image Component
interface ImageProps {
  src: string;
  alt: string;
  width?: number | string;
  height?: number | string;
  className?: string;
  loading?: 'lazy' | 'eager';
  fallback?: string;
  onError?: () => void;
  onLoad?: () => void;
  placeholder?: ReactNode;
  aspectRatio?: 'square' | 'video' | 'wide' | 'ultrawide' | 'custom';
  customRatio?: number;
}

export function Image({
  src,
  alt,
  width,
  height,
  className = "",
  loading = 'lazy',
  fallback,
  onError,
  onLoad,
  placeholder,
  aspectRatio = 'custom',
  customRatio
}: ImageProps) {
  const [imageSrc, setImageSrc] = useState(src);
  const [hasError, setHasError] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoaded, setIsLoaded] = useState(false);

  const aspectRatioClasses = {
    square: 'aspect-square',
    video: 'aspect-video',
    wide: 'aspect-[16/10]',
    ultrawide: 'aspect-[21/9]',
    custom: customRatio ? `aspect-[${customRatio}]` : ''
  };

  const handleError = () => {
    setHasError(true);
    if (fallback && fallback !== imageSrc) {
      setImageSrc(fallback);
    }
    onError?.();
  };

  const handleLoad = () => {
    setIsLoading(false);
    setIsLoaded(true);
    onLoad?.();
  };

  useEffect(() => {
    setImageSrc(src);
    setHasError(false);
    setIsLoading(true);
    setIsLoaded(false);
  }, [src]);

  if (hasError && !fallback) {
    return (
      <div className={cn(
        "flex items-center justify-center bg-gray-100 text-gray-400",
        aspectRatioClasses[aspectRatio],
        className
      )}>
        <div className="text-center">
          <div className="text-4xl mb-2">📷</div>
          <p className="text-sm">Image not available</p>
        </div>
      </div>
    );
  }

  return (
    <div className={cn("relative overflow-hidden", aspectRatioClasses[aspectRatio], className)}>
      {isLoading && placeholder && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-100">
          {placeholder}
        </div>
      )}
      
      <img
        src={imageSrc}
        alt={alt}
        width={width}
        height={height}
        loading={loading}
        onError={handleError}
        onLoad={handleLoad}
        className={cn(
          "w-full h-full object-cover transition-opacity duration-300",
          isLoading ? "opacity-0" : "opacity-100"
        )}
      />
      
      {isLoading && !placeholder && (
        <div className="absolute inset-0 bg-gray-200 animate-pulse" />
      )}
    </div>
  );
}

// Video Component
interface VideoProps {
  src: string;
  poster?: string;
  width?: number | string;
  height?: number | string;
  className?: string;
  controls?: boolean;
  autoplay?: boolean;
  muted?: boolean;
  loop?: boolean;
  preload?: 'none' | 'metadata' | 'auto';
  onPlay?: () => void;
  onPause?: () => void;
  onEnded?: () => void;
  onTimeUpdate?: (currentTime: number) => void;
  onVolumeChange?: (volume: number) => void;
}

export function Video({
  src,
  poster,
  width,
  height,
  className = "",
  controls = true,
  autoplay = false,
  muted = false,
  loop = false,
  preload = 'metadata',
  onPlay,
  onPause,
  onEnded,
  onTimeUpdate,
  onVolumeChange
}: VideoProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMuted] = useState(muted);
  const [isFullscreen, setIsFullscreen] = useState(false);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleTimeUpdate = () => {
      setCurrentTime(video.currentTime);
      onTimeUpdate?.(video.currentTime);
    };

    const handleLoadedMetadata = () => {
      setDuration(video.duration);
    };

    const handleVolumeChange = () => {
      setVolume(video.volume);
      setIsMuted(video.muted);
      onVolumeChange?.(video.volume);
    };

    video.addEventListener('timeupdate', handleTimeUpdate);
    video.addEventListener('loadedmetadata', handleLoadedMetadata);
    video.addEventListener('volumechange', handleVolumeChange);

    return () => {
      video.removeEventListener('timeupdate', handleTimeUpdate);
      video.removeEventListener('loadedmetadata', handleLoadedMetadata);
      video.removeEventListener('volumechange', handleVolumeChange);
    };
  }, [onTimeUpdate, onVolumeChange]);

  const togglePlay = () => {
    const video = videoRef.current;
    if (!video) return;

    if (isPlaying) {
      video.pause();
      setIsPlaying(false);
      onPause?.();
    } else {
      video.play();
      setIsPlaying(true);
      onPlay?.();
    }
  };

  const toggleMute = () => {
    const video = videoRef.current;
    if (!video) return;

    video.muted = !isMuted;
    setIsMuted(!isMuted);
  };

  const toggleFullscreen = () => {
    const video = videoRef.current;
    if (!video) return;

    if (!isFullscreen) {
      if (video.requestFullscreen) {
        video.requestFullscreen();
      }
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    }
    setIsFullscreen(!isFullscreen);
  };

  const seekTo = (time: number) => {
    const video = videoRef.current;
    if (!video) return;

    video.currentTime = time;
    setCurrentTime(time);
  };

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className={cn("relative bg-black rounded-lg overflow-hidden", className)}>
      <video
        ref={videoRef}
        src={src}
        poster={poster}
        width={width}
        height={height}
        controls={false}
        autoplay={autoplay}
        muted={muted}
        loop={loop}
        preload={preload}
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
        onEnded={() => {
          setIsPlaying(false);
          onEnded?.();
        }}
        className="w-full h-full"
      />
      
      {/* Custom Controls */}
      {controls && (
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
          {/* Progress Bar */}
          <div className="mb-3">
            <div className="w-full bg-white/20 rounded-full h-1">
              <div
                className="bg-white h-1 rounded-full transition-all duration-150"
                style={{ width: `${(currentTime / duration) * 100}%` }}
              />
            </div>
            <input
              type="range"
              min={0}
              max={duration || 100}
              value={currentTime}
              onChange={(e) => seekTo(Number(e.target.value))}
              className="w-full h-1 bg-transparent appearance-none cursor-pointer"
              style={{
                background: `linear-gradient(to right, white 0%, white ${(currentTime / duration) * 100}%, rgba(255,255,255,0.3) ${(currentTime / duration) * 100}%, rgba(255,255,255,0.3) 100%)`
              }}
            />
          </div>
          
          {/* Control Buttons */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={togglePlay}
                className="text-white hover:text-gray-300 transition-colors"
              >
                {isPlaying ? (
                  <PauseIcon className="h-6 w-6" />
                ) : (
                  <PlayIcon className="h-6 w-6" />
                )}
              </button>
              
              <div className="flex items-center space-x-2 text-white text-sm">
                <span>{formatTime(currentTime)}</span>
                <span>/</span>
                <span>{formatTime(duration)}</span>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <button
                onClick={toggleMute}
                className="text-white hover:text-gray-300 transition-colors"
              >
                {isMuted ? (
                  <SpeakerXMarkIcon className="h-5 w-5" />
                ) : (
                  <SpeakerWaveIcon className="h-5 w-5" />
                )}
              </button>
              
              <button
                onClick={toggleFullscreen}
                className="text-white hover:text-gray-300 transition-colors"
              >
                {isFullscreen ? (
                  <ArrowsPointingInIcon className="h-5 w-5" />
                ) : (
                  <ArrowsPointingOutIcon className="h-5 w-5" />
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Audio Component
interface AudioProps {
  src: string;
  className?: string;
  controls?: boolean;
  autoplay?: boolean;
  muted?: boolean;
  loop?: boolean;
  preload?: 'none' | 'metadata' | 'auto';
  onPlay?: () => void;
  onPause?: () => void;
  onEnded?: () => void;
  onTimeUpdate?: (currentTime: number) => void;
  onVolumeChange?: (volume: number) => void;
}

export function Audio({
  src,
  className = "",
  controls = true,
  autoplay = false,
  muted = false,
  loop = false,
  preload = 'metadata',
  onPlay,
  onPause,
  onEnded,
  onTimeUpdate,
  onVolumeChange
}: AudioProps) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMuted] = useState(muted);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handleTimeUpdate = () => {
      setCurrentTime(audio.currentTime);
      onTimeUpdate?.(audio.currentTime);
    };

    const handleLoadedMetadata = () => {
      setDuration(audio.duration);
    };

    const handleVolumeChange = () => {
      setVolume(audio.volume);
      setIsMuted(audio.muted);
      onVolumeChange?.(audio.volume);
    };

    audio.addEventListener('timeupdate', handleTimeUpdate);
    audio.addEventListener('loadedmetadata', handleLoadedMetadata);
    audio.addEventListener('volumechange', handleVolumeChange);

    return () => {
      audio.removeEventListener('timeupdate', handleTimeUpdate);
      audio.removeEventListener('loadedmetadata', handleLoadedMetadata);
      audio.removeEventListener('volumechange', handleVolumeChange);
    };
  }, [onTimeUpdate, onVolumeChange]);

  const togglePlay = () => {
    const audio = audioRef.current;
    if (!audio) return;

    if (isPlaying) {
      audio.pause();
      setIsPlaying(false);
      onPause?.();
    } else {
      audio.play();
      setIsPlaying(true);
      onPlay?.();
    }
  };

  const toggleMute = () => {
    const audio = audioRef.current;
    if (!audio) return;

    audio.muted = !isMuted;
    setIsMuted(!isMuted);
  };

  const seekTo = (time: number) => {
    const audio = audioRef.current;
    if (!audio) return;

    audio.currentTime = time;
    setCurrentTime(time);
  };

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className={cn("bg-white rounded-lg shadow-sm border border-gray-200 p-4", className)}>
      <audio
        ref={audioRef}
        src={src}
        controls={false}
        autoplay={autoplay}
        muted={muted}
        loop={loop}
        preload={preload}
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
        onEnded={() => {
          setIsPlaying(false);
          onEnded?.();
        }}
      />
      
      {/* Custom Controls */}
      {controls && (
        <div className="space-y-3">
          {/* Progress Bar */}
          <div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-op-blue h-2 rounded-full transition-all duration-150"
                style={{ width: `${(currentTime / duration) * 100}%` }}
              />
            </div>
            <input
              type="range"
              min={0}
              max={duration || 100}
              value={currentTime}
              onChange={(e) => seekTo(Number(e.target.value))}
              className="w-full h-2 bg-transparent appearance-none cursor-pointer"
              style={{
                background: `linear-gradient(to right, #3B82F6 0%, #3B82F6 ${(currentTime / duration) * 100}%, #E5E7EB ${(currentTime / duration) * 100}%, #E5E7EB 100%)`
              }}
            />
          </div>
          
          {/* Control Buttons */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={togglePlay}
                className="p-2 bg-op-blue text-white rounded-full hover:bg-op-blue-700 transition-colors"
              >
                {isPlaying ? (
                  <PauseIcon className="h-5 w-5" />
                ) : (
                  <PlayIcon className="h-5 w-5" />
                )}
              </button>
              
              <div className="flex items-center space-x-2 text-gray-600 text-sm">
                <span>{formatTime(currentTime)}</span>
                <span>/</span>
                <span>{formatTime(duration)}</span>
              </div>
            </div>
            
            <button
              onClick={toggleMute}
              className="p-2 text-gray-600 hover:text-gray-800 transition-colors"
            >
              {isMuted ? (
                <SpeakerXMarkIcon className="h-5 w-5" />
              ) : (
                <SpeakerWaveIcon className="h-5 w-5" />
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

// Media Gallery Component
interface MediaItem {
  id: string;
  type: 'image' | 'video' | 'audio';
  src: string;
  alt?: string;
  poster?: string;
  thumbnail?: string;
}

interface MediaGalleryProps {
  items: MediaItem[];
  className?: string;
  showThumbnails?: boolean;
  autoPlay?: boolean;
  loop?: boolean;
  onItemClick?: (item: MediaItem, index: number) => void;
}

export function MediaGallery({
  items,
  className = "",
  showThumbnails = true,
  autoPlay = false,
  loop = true,
  onItemClick
}: MediaGalleryProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const currentItem = items[currentIndex];

  const goToNext = () => {
    if (currentIndex < items.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else if (loop) {
      setCurrentIndex(0);
    }
  };

  const goToPrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    } else if (loop) {
      setCurrentIndex(items.length - 1);
    }
  };

  const goToItem = (index: number) => {
    setCurrentIndex(index);
  };

  useEffect(() => {
    if (!autoPlay) return;

    const interval = setInterval(() => {
      goToNext();
    }, 5000);

    return () => clearInterval(interval);
  }, [currentIndex, autoPlay, loop]);

  if (items.length === 0) {
    return (
      <div className={cn("text-center py-12 text-gray-500", className)}>
        No media items available
      </div>
    );
  }

  return (
    <div className={cn("space-y-4", className)}>
      {/* Main Media Display */}
      <div className="relative bg-black rounded-lg overflow-hidden">
        {currentItem.type === 'image' && (
          <Image
            src={currentItem.src}
            alt={currentItem.alt || ''}
            className="w-full h-96 object-contain"
          />
        )}
        
        {currentItem.type === 'video' && (
          <Video
            src={currentItem.src}
            poster={currentItem.poster}
            className="w-full h-96"
            controls
            autoplay={autoPlay}
            loop={loop}
          />
        )}
        
        {currentItem.type === 'audio' && (
          <div className="flex items-center justify-center h-96">
            <Audio
              src={currentItem.src}
              className="w-full max-w-md"
              controls
              autoplay={autoPlay}
              loop={loop}
            />
          </div>
        )}
        
        {/* Navigation Arrows */}
        {items.length > 1 && (
          <>
            <button
              onClick={goToPrevious}
              className="absolute left-4 top-1/2 transform -translate-y-1/2 p-2 bg-black/50 text-white rounded-full hover:bg-black/70 transition-colors"
            >
              <BackwardIcon className="h-5 w-5" />
            </button>
            
            <button
              onClick={goToNext}
              className="absolute right-4 top-1/2 transform -translate-y-1/2 p-2 bg-black/50 text-white rounded-full hover:bg-black/70 transition-colors"
            >
              <ForwardIcon className="h-5 w-5" />
            </button>
          </>
        )}
        
        {/* Counter */}
        <div className="absolute top-4 right-4 bg-black/50 text-white px-2 py-1 rounded text-sm">
          {currentIndex + 1} / {items.length}
        </div>
      </div>
      
      {/* Thumbnails */}
      {showThumbnails && items.length > 1 && (
        <div className="flex space-x-2 overflow-x-auto">
          {items.map((item, index) => (
            <button
              key={item.id}
              onClick={() => goToItem(index)}
              className={cn(
                "flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 transition-all",
                index === currentIndex
                  ? "border-op-blue ring-2 ring-op-blue/20"
                  : "border-gray-200 hover:border-gray-300"
              )}
            >
              {item.type === 'image' && (
                <Image
                  src={item.thumbnail || item.src}
                  alt={item.alt || ''}
                  className="w-full h-full object-cover"
                />
              )}
              
              {item.type === 'video' && (
                <div className="relative w-full h-full bg-gray-100 flex items-center justify-center">
                  <PlayIcon className="h-6 w-6 text-gray-400" />
                  {item.poster && (
                    <Image
                      src={item.poster}
                      alt={item.alt || ''}
                      className="absolute inset-0 w-full h-full object-cover"
                    />
                  )}
                </div>
              )}
              
              {item.type === 'audio' && (
                <div className="w-full h-full bg-gray-100 flex items-center justify-center">
                  <SpeakerWaveIcon className="h-6 w-6 text-gray-400" />
                </div>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
