import React, { useState } from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';

const Container = styled.div`
  position: fixed;
  top: 0;
  width: 100%;
  height: 70px;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 50px;
  z-index: 10;
`;

const Logo = styled.h1`
  color: red;
  font-size: 2rem;
  cursor: pointer;
`;

const Nav = styled.nav`
  display: flex;
  gap: 20px;
`;

const NavItem = styled.a`
  color: white;
  text-decoration: none;
  &:hover {
    color: red;
  }
`;

const User = styled.div`
  color: white;
  cursor: pointer;
  position: relative;
`;

const Menu = styled.div`
  position: absolute;
  top: 100%;
  right: 0;
  background: #333;
  border: 1px solid #555;
  border-radius: 5px;
  padding: 10px;
  display: ${props => props.show ? 'block' : 'none'};
`;

const MenuItem = styled.div`
  color: white;
  cursor: pointer;
  padding: 5px 0;
  &:hover {
    color: red;
  }
`;

const Header = () => {
  const [showMenu, setShowMenu] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  return (
    <Container>
      <Logo onClick={() => navigate('/browse')}>Netflix</Logo>
      <Nav>
        <NavItem onClick={() => navigate('/browse')}>Home</NavItem>
        <NavItem onClick={() => navigate('/mylist')}>My List</NavItem>
        <NavItem onClick={() => navigate('/recommend')}>Recommend Movie</NavItem>
      </Nav>
      <User onClick={() => setShowMenu(!showMenu)}>
        👤
        <Menu show={showMenu}>
          <MenuItem onClick={handleLogout}>Logout</MenuItem>
        </Menu>
      </User>
    </Container>
  );
};

export default Header;