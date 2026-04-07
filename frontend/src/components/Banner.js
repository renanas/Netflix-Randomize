import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  position: relative;
  height: 70vh;
  background-size: cover;
  background-position: center;
  background-image: url(${props => props.bgImage || 'https://via.placeholder.com/1920x1080'});
`;

const Overlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right, rgba(0,0,0,0.8), transparent);
`;

const Content = styled.div`
  position: absolute;
  bottom: 20%;
  left: 50px;
  color: white;
  max-width: 500px;
`;

const Title = styled.h1`
  font-size: 3rem;
  margin-bottom: 1rem;
`;

const Description = styled.p`
  font-size: 1.2rem;
  margin-bottom: 2rem;
`;

const Buttons = styled.div`
  display: flex;
  gap: 1rem;
`;

const Button = styled.button`
  padding: 0.5rem 2rem;
  background: ${props => props.primary ? 'white' : 'rgba(255,255,255,0.3)'};
  color: ${props => props.primary ? 'black' : 'white'};
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
`;

const Banner = ({ movie }) => {
  if (!movie) return null;

  const bgImage = movie.backdrop_path ? `https://image.tmdb.org/t/p/original${movie.backdrop_path}` : null;

  return (
    <Container bgImage={bgImage}>
      <Overlay />
      <Content>
        <Title>{movie.title}</Title>
        <Description>{movie.overview}</Description>
        <Buttons>
          <Button primary>Play</Button>
          <Button>My List</Button>
        </Buttons>
      </Content>
    </Container>
  );
};

export default Banner;