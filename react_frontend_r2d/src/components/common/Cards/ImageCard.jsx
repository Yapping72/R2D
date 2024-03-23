import React, { useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import './ImageCard.css'; // Import CSS file for custom styles

export default function ImageCard({ title, description, imageUrl }) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <Card className={`custom-card ${isHovered ? 'hovered' : ''}`} onMouseEnter={() => setIsHovered(true)} onMouseLeave={() => setIsHovered(false)}>
      <Typography variant="h5" component="h2" className="title">
        {title}
      </Typography>
      <CardMedia component="img" src={imageUrl} className={`card-media ${isHovered ? 'hovered' : ''}`} />
      <CardContent className={`card-content ${isHovered ? 'hovered' : ''}`}>
        <Typography variant="h6"color="text.secondary" className="description">
        {description}
        </Typography>
      </CardContent>
    </Card>
  );
}
