import React, { useState, useEffect } from 'react';
import Typography from '@mui/material/Typography';
import './TypingAnimation.css'; // Make sure you have the corresponding CSS for the cursor

const TypingAnimation = ({ text, variant = 'h1' }) => {
  const [displayText, setDisplayText] = useState('');
  const [showCursor, setShowCursor] = useState(false);
  const [restartAnimation, setRestartAnimation] = useState(false); // Added for animation restart

  useEffect(() => {
    let index = 0;
    const typingInterval = setInterval(() => {
      setDisplayText(text.substring(0, index));
      setShowCursor(true);
      index++;
      if (index > text.length) {
        clearInterval(typingInterval);
        setShowCursor(false);
      }
    }, 80); // Adjust typing speed by changing the interval duration

    return () => clearInterval(typingInterval);
  }, [text, restartAnimation]); // Depend on restartAnimation to restart typing

  const handleMouseEnter = () => {
    setDisplayText(''); // Reset displayText to start typing animation from scratch
    setRestartAnimation(!restartAnimation); // Toggle to restart the animation
  };

  return (
    <div className="typing-animation" onMouseEnter={handleMouseEnter}>
      <Typography variant={variant} component={variant}>{displayText}</Typography>
      {showCursor && <div className="cursor" />}
    </div>
  );
};

export default TypingAnimation;
