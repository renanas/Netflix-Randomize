import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import axios from 'axios';

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: #000;
  color: white;
`;

const Logo = styled.h1`
  font-size: 3rem;
  margin-bottom: 2rem;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  width: 300px;
`;

const Input = styled.input`
  padding: 1rem;
  margin-bottom: 1rem;
  border: none;
  border-radius: 5px;
`;

const Button = styled.button`
  padding: 1rem;
  background: red;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
`;

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/netflix-randomize/login', { email, password });
      localStorage.setItem('token', response.data.access_token);
      // Assume success, navigate to home
      navigate('/browse');
    } catch (error) {
      alert('Login failed');
    }
  };

  return (
    <Container>
      <Logo>Netflix Randomize</Logo>
      <Form onSubmit={handleSubmit}>
        <Input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <Input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <Button type="submit">Entrar</Button>
      </Form>
    </Container>
  );
};

export default Login;