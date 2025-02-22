import React, { useState, useEffect } from "react";
import { LineChart, Smartphone } from "lucide-react";
import goldenApple from "../assets/golden_apple.png";

interface ButtonProps {
  label: string;
  icon?: React.ReactNode;
  onClick?: () => void;
}

interface BouncingImageProps {
  delay: number;
  initialX: number;
  initialY: number;
}

const PrimaryButton: React.FC<ButtonProps> = ({ label, icon, onClick }) => (
  <button
    onClick={onClick}
    className="flex items-center gap-2 px-6 py-3 bg-yellow-500 text-white rounded-lg hover:bg-yellow-400 transition-colors">
    {icon}
    <span>{label}</span>
  </button>
);

const BouncingImage: React.FC<BouncingImageProps> = ({
  delay,
  initialX,
  initialY,
}) => {
  const [position, setPosition] = useState({ x: initialX, y: initialY });

  useEffect(() => {
    const moveImage = () => {
      const newX = Math.random() * (window.innerWidth - 100);
      const newY = Math.random() * (window.innerHeight - 100);
      setPosition({ x: newX, y: newY });
    };

    // Initial delay before starting animation
    const initialTimeout = setTimeout(() => {
      moveImage();
      // Start regular interval after initial delay
      const interval = setInterval(moveImage, 3000);
      return () => clearInterval(interval);
    }, delay);

    return () => clearTimeout(initialTimeout);
  }, [delay]);

  return (
    <div
      className="absolute w-16 h-16 transition-all duration-3000 ease-in-out"
      style={{
        left: position.x,
        top: position.y,
        transitionDuration: "3000ms",
      }}>
      <img
        src={goldenApple}
        alt="Bouncing Apple"
        className="w-full h-full object-contain animate-pulse"
      />
    </div>
  );
};

const BackgroundImages: React.FC = () => {
  const images = [
    { delay: 0, x: 100, y: 100 },
    { delay: 1000, x: 300, y: 200 },
    { delay: 2000, x: 500, y: 300 },
    { delay: 2000, x: 500, y: 300 },
    { delay: 2000, x: 500, y: 300 },
    { delay: 3000, x: 700, y: 400 },
    { delay: 3000, x: 700, y: 400 },
    { delay: 4000, x: 200, y: 500 },
    { delay: 4000, x: 200, y: 500 },
    { delay: 4000, x: 200, y: 500 },
  ];

  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden">
      {images.map((img, index) => (
        <BouncingImage
          key={index}
          delay={img.delay}
          initialX={img.x}
          initialY={img.y}
        />
      ))}
    </div>
  );
};

const LandingPage: React.FC = () => {
  return (
    <div className="relative min-h-screen bg-gradient-to-br from-yellow-100 to-white overflow-hidden">
      <BackgroundImages />

      <div className="relative container mx-auto px-4 py-16 z-10">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-yellow-600 mb-4">
            The Golden Apple
          </h1>
          <p className="text-xl text-gray-600">
            iPhone Market Analytics Made Simple
          </p>
        </div>

        {/* Main Actions */}
        <div className="max-w-md mx-auto space-y-6">
          <div className="bg-white/80 backdrop-blur-sm p-8 rounded-xl shadow-lg">
            <div className="space-y-4">
              <PrimaryButton
                label="Market Analysis"
                icon={<LineChart className="w-5 h-5" />}
              />

              <PrimaryButton
                label="iPhone Models"
                icon={<Smartphone className="w-5 h-5" />}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
