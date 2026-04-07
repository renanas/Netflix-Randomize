// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// Storage keys
const STORAGE_KEYS = {
    TOKEN: 'netflix_token',
    USER_ID: 'netflix_user_id'
};

// Helper function to get auth headers
function getAuthHeaders() {
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
}

// API calls
const API = {
    // Auth
    login: async (email, password) => {
        const response = await fetch(`${API_BASE_URL}/netflix-randomize/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        if (!response.ok) throw new Error('Login failed');
        return response.json();
    },

    // Recommendations
    getRecommendations: async () => {
        const response = await fetch(`${API_BASE_URL}/netflix-randomize/recommendationMovie`, {
            method: 'GET',
            headers: getAuthHeaders()
        });
        if (!response.ok) throw new Error('Failed to fetch recommendations');
        return response.json();
    },

    getRandomMovie: async () => {
        const response = await fetch(`${API_BASE_URL}/netflix-randomize/randomMovie`, {
            method: 'GET',
            headers: getAuthHeaders()
        });
        if (!response.ok) throw new Error('Failed to fetch random movie');
        return response.json();
    },

    refreshRecommendations: async () => {
        const response = await fetch(`${API_BASE_URL}/netflix-randomize/recommendationMovie/refresh`, {
            method: 'POST',
            headers: getAuthHeaders()
        });
        if (!response.ok) throw new Error('Failed to refresh recommendations');
        return response.json();
    }
};

// Check if user is authenticated
function isAuthenticated() {
    return !!localStorage.getItem(STORAGE_KEYS.TOKEN);
}

// Logout
function logout() {
    localStorage.removeItem(STORAGE_KEYS.TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER_ID);
    window.location.href = 'index.html';
}
