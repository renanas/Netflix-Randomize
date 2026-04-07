import React from 'react';
import styled from 'styled-components';
import MovieCard from './MovieCard';

const Container = styled.div`
  margin-left: 50px;
  margin-bottom: 2rem;
`;

const Title = styled.h2`
  color: white;
  margin-bottom: 1rem;
`;

const MoviesContainer = styled.div`
  display: flex;
  overflow-x: scroll;
  gap: 10px;
  &::-webkit-scrollbar {
    display: none;
  }
`;

const Row = ({ title, movies }) => {
  return (
    <Container>
      <Title>{title}</Title>
      <MoviesContainer>
        {movies.map(movie => (
          <MovieCard key={movie.id} movie={movie} />
        ))}
      </MoviesContainer>
    </Container>
  );
};

export default Row;