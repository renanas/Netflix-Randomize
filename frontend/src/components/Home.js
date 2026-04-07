import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import Header from './Header';
import Banner from './Banner';
import Row from './Row';

const Container = styled.div`
  background: #111;
  color: white;
  padding-top: 70px; /* Account for fixed header */
`;

const Home = () => {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await axios.get('/netflix-randomize/movies');
        setMovies(response.data.movies);
      } catch (error) {
        console.error('Error fetching movies:', error);
      }
    };
    fetchMovies();
  }, []);

  return (
    <Container>
      <Header />
      <Banner movie={movies[0]} />
      <Row title="Trending Now" movies={movies.slice(0, 10)} />
      <Row title="Top Rated" movies={movies.slice(10, 20)} />
      <Row title="Action Movies" movies={movies.slice(20, 30)} />
    </Container>
  );
};

export default Home;