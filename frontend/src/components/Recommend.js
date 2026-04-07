import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import Header from './Header';

const Container = styled.div`
  background: #111;
  color: white;
  padding-top: 70px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
`;

const CarouselContainer = styled.div`
  position: relative;
  width: 80%;
  height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const MovieCard = styled.div`
  width: 300px;
  height: 450px;
  background-size: cover;
  background-position: center;
  border-radius: 10px;
  background-image: url(${props => props.bgImage});
`;

const MovieDetails = styled.div`
  margin-top: 20px;
  text-align: center;
  max-width: 600px;
`;

const Title = styled.h1`
  font-size: 2rem;
  margin-bottom: 1rem;
`;

const Overview = styled.p`
  font-size: 1rem;
  margin-bottom: 1rem;
`;

const Rating = styled.p`
  font-size: 1.2rem;
  color: #ffd700;
`;

const Button = styled.button`
  padding: 10px 20px;
  background: red;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 20px;
`;

const Recommend = () => {
  const [movies, setMovies] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const fetchRandomMovies = async () => {
      const token = localStorage.getItem('token');
      if (!token) return;
      try {
        const promises = [];
        for (let i = 0; i < 10; i++) { // Fetch 10 random movies
          promises.push(
            axios.get('/netflix-randomize/randomMovie', {
              headers: { Authorization: `Bearer ${token}` }
            })
          );
        }
        const responses = await Promise.all(promises);
        const data = responses.map(res => res.data).filter(movie => movie && movie.id);
        // Remove duplicates if any
        const unique = data.filter((movie, index, self) => self.findIndex(m => m.id === movie.id) === index);
        setMovies(unique);
        setCurrentIndex(0);
      } catch (error) {
        console.error('Error fetching random movies:', error);
        // Fallback to popular movies
        try {
          const popularResponse = await axios.get('/netflix-randomize/movies?limit=20');
          const data = popularResponse.data.movies || [];
          setMovies(data);
          setCurrentIndex(0);
        } catch (popularError) {
          console.error('Error fetching popular movies:', popularError);
        }
      }
    };
    fetchRandomMovies();
  }, []);

  const handleSpinAgain = () => {
    setCurrentIndex((prev) => (prev + 1) % movies.length);
  };

  if (movies.length === 0) return <Container><Header />Loading...</Container>;

  const currentMovie = movies[currentIndex];

  if (!currentMovie) return <Container><Header />No recommendations available.</Container>;

  return (
    <Container>
      <Header />
      <CarouselContainer>
        <MovieCard bgImage={currentMovie.poster_path ? `https://image.tmdb.org/t/p/w500${currentMovie.poster_path}` : 'https://via.placeholder.com/300x450'} />
      </CarouselContainer>
      <MovieDetails>
        <Title>{currentMovie.title}</Title>
        <Overview>{currentMovie.overview}</Overview>
        <Rating>Rating: {currentMovie.vote_average}/10</Rating>
        <Button onClick={handleSpinAgain}>Next Random Movie</Button>
      </MovieDetails>
    </Container>
  );
};

export default Recommend;