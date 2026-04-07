import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import Header from './Header';
import Row from './Row';

const Container = styled.div`
  background: #111;
  color: white;
  padding-top: 70px; /* Account for fixed header */
`;

const MyList = () => {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    const fetchWatchlist = async () => {
      const token = localStorage.getItem('token');
      if (!token) return;
      try {
        const response = await axios.get('/netflix-randomize/watchlist/detailed', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setMovies(response.data.my_list || []);
      } catch (error) {
        console.error('Error fetching watchlist:', error);
      }
    };
    fetchWatchlist();
  }, []);

  return (
    <Container>
      <Header />
      <Row title="My List" movies={movies} />
    </Container>
  );
};

export default MyList;