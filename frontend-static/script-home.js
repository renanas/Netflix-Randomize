// Home Page Script
let recommendedMovies = [];
let isSpinning = false;

document.addEventListener('DOMContentLoaded', async () => {
    // Redirect if not authenticated
    if (!isAuthenticated()) {
        window.location.href = 'index.html';
        return;
    }

    // Set up event listeners
    document.getElementById('logoutBtn').addEventListener('click', logout);
    document.getElementById('spinBtn').addEventListener('click', spinRoulette);
    document.getElementById('refreshBtn').addEventListener('click', refreshRecommendations);

    // Load initial data
    await loadRecommendations();
});

// Load recommendations from API
async function loadRecommendations() {
    try {
        showLoading(true);
        const movies = await API.getRecommendations();
        recommendedMovies = movies;
        displayMovies(movies);
    } catch (error) {
        console.error('Error loading recommendations:', error);
        document.getElementById('moviesContainer').innerHTML = 
            '<div class="loading">❌ Erro ao carregar filmes. Tente novamente.</div>';
    } finally {
        showLoading(false);
    }
}

// Refresh recommendations
async function refreshRecommendations() {
    const btn = document.getElementById('refreshBtn');
    btn.disabled = true;
    
    try {
        showLoading(true);
        const movies = await API.refreshRecommendations();
        recommendedMovies = movies;
        displayMovies(movies);
    } catch (error) {
        console.error('Error refreshing recommendations:', error);
    } finally {
        showLoading(false);
        btn.disabled = false;
    }
}

// Display movies in grid
function displayMovies(movies) {
    const container = document.getElementById('moviesContainer');
    
    if (!movies || movies.length === 0) {
        container.innerHTML = '<div class="loading">Nenhum filme recomendado encontrado.</div>';
        return;
    }

    container.innerHTML = movies.map(movie => createMovieCard(movie)).join('');
}

// Create movie card HTML
function createMovieCard(movie) {
    const title = movie.title || movie.name || 'Sem título';
    const rating = movie.vote_average ? `⭐ ${movie.vote_average.toFixed(1)}/10` : 'Sem avaliação';
    const genres = movie.genre_ids ? `Gêneros: ${movie.genre_ids.join(', ')}` : '';
    const popularity = movie.popularity ? `👁 ${Math.round(movie.popularity)} visualizações` : '';

    return `
        <div class="movie-card">
            <div class="movie-poster">
                ${movie.poster_path ? `<img src="https://image.tmdb.org/t/p/w200${movie.poster_path}" alt="${title}">` : '🎬'}
            </div>
            <div class="movie-info">
                <div class="movie-title" title="${title}">${title}</div>
                <div class="movie-rating">${rating}</div>
                <div class="movie-genres" title="${genres}">${genres || popularity}</div>
            </div>
        </div>
    `;
}

// Spin roulette
async function spinRoulette() {
    if (isSpinning || recommendedMovies.length === 0) return;

    isSpinning = true;
    const spinBtn = document.getElementById('spinBtn');
    const wheel = document.getElementById('rouletteWheel');
    const resultDiv = document.getElementById('randomMovieResult');
    const resultMovie = document.getElementById('resultMovie');

    // Disable button
    spinBtn.disabled = true;
    spinBtn.textContent = '⏳ Girando...';

    // Hide previous result
    resultDiv.classList.add('hidden');

    // Add spinning animation
    wheel.classList.add('spinning');

    // Calculate random rotation (adds 2160 degrees = 6 full rotations + random angle)
    const randomAngle = Math.random() * 360;
    const totalRotation = 2160 + randomAngle;

    try {
        // Wait for animation to complete
        await new Promise(resolve => setTimeout(resolve, 4000));

        // Get random movie from API
        showLoading(true);
        const randomMovie = await API.getRandomMovie();

        // Remove spinning animation
        wheel.classList.remove('spinning');
        wheel.style.transform = `rotate(${totalRotation}deg)`;

        // Display result
        displayRandomMovieResult(randomMovie);
        resultDiv.classList.remove('hidden');

        // Scroll to result
        resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    } catch (error) {
        console.error('Error getting random movie:', error);
        wheel.classList.remove('spinning');
        resultMovie.innerHTML = '<p style="color: var(--error-color);">❌ Erro ao selecionar filme. Tente novamente.</p>';
        resultDiv.classList.remove('hidden');
    } finally {
        showLoading(false);
        spinBtn.disabled = false;
        spinBtn.textContent = '🎲 GIRAR & DESCOBRIR';
        isSpinning = false;
    }
}

// Display random movie result
function displayRandomMovieResult(movie) {
    const resultMovie = document.getElementById('resultMovie');
    const title = movie.title || movie.name || 'Sem título';
    const rating = movie.vote_average ? `.0/10` : 'Sem avaliação';
    const genres = movie.genre_ids ? movie.genre_ids.join(', ') : 'Gênero desconhecido';
    const overview = movie.overview || 'Sem descrição disponível';
    const popularity = movie.popularity ? Math.round(movie.popularity) : 0;

    resultMovie.innerHTML = `
        <div>
            <h4>${title}</h4>
            <p><strong>⭐ Avaliação:</strong> ${rating}</p>
            <p><strong>📂 Gêneros:</strong> ${genres}</p>
            <p><strong>👁 Popularidade:</strong> ${popularity} visualizações</p>
            <p><strong>📝 Sinopse:</strong> ${overview}</p>
        </div>
    `;
}

// Show/hide loading overlay
function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (show) {
        overlay.classList.remove('hidden');
    } else {
        overlay.classList.add('hidden');
    }
}
