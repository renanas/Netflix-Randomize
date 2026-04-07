import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  min-width: 200px;
  height: 300px;
  background: #333;
  border-radius: 5px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s;
  &:hover {
    transform: scale(1.05);
  }
`;

const Image = styled.img`
  width: 100%;
  height: 100%;
  object-fit: cover;
`;

const MovieCard = ({ movie }) => {
  const posterUrl = movie.poster_path ? `https://image.tmdb.org/t/p/w500${movie.poster_path}` : 'https://via.placeholder.com/200x300';

  return (
    <Container>
      <Image src={posterUrl} alt={movie.title} />
    </Container>
  );
};

export default MovieCard;