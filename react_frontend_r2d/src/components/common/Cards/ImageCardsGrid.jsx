// CardsGrid.jsx
import React from 'react';
import Grid from '@mui/material/Grid';
import ImageCard from './ImageCard'; // Import your ImageCard component

const CardsGrid = ({ cards }) => {
  return (
    <>
    <Grid container spacing={3} justifyContent="center"> {/* justifyContent centers the cards horizontally */}
      {cards.map((card, index) => (
        <Grid item key={index} xs={12} sm={6} md={4} lg={3}>
          <ImageCard 
            title={card.title} 
            description={card.description} 
            imageUrl={card.imageUrl} 
          />
        </Grid>
      ))}
    </Grid>
    </>
  );
};

export default CardsGrid;
