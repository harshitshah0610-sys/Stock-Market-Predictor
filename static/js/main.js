 // ================================================
// AI Stock Market Predictor - Main JavaScript
// ================================================

// Chart.js configuration
let priceChart = null;
let currentSymbol = 'AAPL';
let currentExchange = 'US';
let allStocks = { US: {}, NSE: {}, BSE: {} };

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initParticles();
    loadStockList();
    initEventListeners();
    loadAllEvents();
    updateLastUpdateTime();
    loadStockData(currentSymbol);
    
    // Auto-refresh every 60 seconds
    setInterval(() => {
        loadStockData(currentSymbol);
        updateLastUpdateTime();
    }, 60000);
});

// Create particle background
function initParticles() {
    const container = document.getElementById('particles');
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 15 + 's';
        particle.style.animationDuration = (10 + Math.random() * 10) + 's';
        
        const colors = ['#00ff88', '#00d4ff', '#ff3366', '#ffd700'];
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];
        
        container.appendChild(particle);
    }
}

// Load stock list from API
async function loadStockList() {
    try {
        const response = await fetch('/api/stocks');
        allStocks = await response.json();
        populateStockSelector();
    } catch (error) {
        console.error('Failed to load stock list:', error);
    }
}

// Populate stock selector based on current exchange
function populateStockSelector() {
    const select = document.getElementById('stockSelect');
    select.innerHTML = '';
    
    const stocks = allStocks[currentExchange] || {};
    
    Object.keys(stocks).forEach(symbol => {
        const option = document.createElement('option');
        option.value = symbol;
        option.textContent = `${symbol} - ${stocks[symbol].name}`;
        if (symbol === currentSymbol) option.selected = true;
        select.appendChild(option);
    });
}

// Initialize event listeners
function initEventListeners() {
    // Exchange tabs
    const exchangeBtns = document.querySelectorAll('.exchange-btn');
    exchangeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            exchangeBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentExchange = btn.dataset.exchange;
            
            // Set first stock of that exchange
            const stocks = allStocks[currentExchange];
            if (stocks) {
                currentSymbol = Object.keys(stocks)[0];
            }
            
            populateStockSelector();
            loadStockData(currentSymbol);
        });
    });
    
    // Stock selector
    const stockSelect = document.getElementById('stockSelect');
    stockSelect.addEventListener('change', (e) => {
        currentSymbol = e.target.value;
        loadStockData(currentSymbol);
    });
    
    // Timeframe buttons - get active timeframe and pass to API
    const tfButtons = document.querySelectorAll('.tf-btn');
    tfButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            tfButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const timeframe = btn.dataset.tf;
            loadStockData(currentSymbol, timeframe);
        });
    });
    
    // Search functionality
    const searchInput = document.getElementById('stockSearch');
    const searchResults = document.getElementById('searchResults');
    
    searchInput.addEventListener('input', async (e) => {
        const query = e.target.value;
        if (query.length < 1) {
            searchResults.style.display = 'none';
            return;
        }
        
        try {
            const response = await fetch(`/api/search/${query}`);
            const results = await response.json();
            
            if (results.length > 0) {
                searchResults.innerHTML = '';
                results.slice(0, 10).forEach(stock => {
                    const item = document.createElement('div');
                    item.className = 'search-result-item';
                    item.innerHTML = `
                        <span class="search-symbol">${stock.symbol}</span>
                        <span class="search-name">${stock.name}</span>
                        <span class="search-exchange">${stock.exchange}</span>
                    `;
                    item.addEventListener('click', () => {
                        currentSymbol = stock.symbol;
                        currentExchange = stock.exchange;
                        
                        // Update UI
                        document.querySelectorAll('.exchange-btn').forEach(b => {
                            b.classList.toggle('active', b.dataset.exchange === currentExchange);
                        });
                        
                        populateStockSelector();
                        document.getElementById('stockSelect').value = currentSymbol;
                        searchInput.value = '';
                        searchResults.style.display = 'none';
                        loadStockData(currentSymbol);
                    });
                    searchResults.appendChild(item);
                });
                searchResults.style.display = 'block';
            } else {
                searchResults.style.display = 'none';
            }
        } catch (error) {
            console.error('Search error:', error);
        }
    });
    
    // Close search on outside click
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.stock-search')) {
            searchResults.style.display = 'none';
        }
    });
}

// Update last update time
function updateLastUpdateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('lastUpdate').textContent = timeString;
}

// Real-time price update - fetches every second when market is open
let realtimeInterval = null;
let currentPrice = 0;

async function startRealtimePriceUpdates(symbol) {
    // Clear any existing interval
    if (realtimeInterval) {
        clearInterval(realtimeInterval);
    }
    
    // Update immediately
    await updateRealtimePrice(symbol);
    
    // Then update every second
    realtimeInterval = setInterval(async () => {
        await updateRealtimePrice(symbol);
    }, 1000);
}

async function updateRealtimePrice(symbol) {
    try {
        const response = await fetch(`/api/price/${symbol}`);
        const data = await response.json();
        
        if (data.error) {
            console.log('Price update error:', data.error);
            return;
        }
        
        // Update price display
        const priceElement = document.getElementById('stockPrice');
        const changeElement = document.getElementById('stockChange');
        
        const oldPrice = currentPrice;
        currentPrice = data.current_price;
        
        priceElement.textContent = data.current_price_formatted;
        
        // Calculate and show change
        if (oldPrice > 0 && oldPrice !== currentPrice) {
            const priceChange = currentPrice - oldPrice;
            const changePercent = (priceChange / oldPrice) * 100;
            const changeSign = priceChange >= 0 ? '+' : '';
            changeElement.textContent = changeSign + changePercent.toFixed(2) + '%';
            changeElement.className = 'stock-change' + (priceChange < 0 ? ' negative' : '');
            
            // Add flash animation
            priceElement.style.color = priceChange >= 0 ? '#00ff88' : '#ff3366';
            setTimeout(() => {
                priceElement.style.color = '';
            }, 500);
        }
        
        // Update market status indicator
        const statusDot = document.querySelector('.status-dot');
        const statusText = document.querySelector('.status-text');
        if (data.is_market_open) {
            statusDot.style.background = '#00ff88';
            statusText.textContent = 'Market Open';
        } else {
            statusDot.style.background = '#ff8c00';
            statusText.textContent = 'Market Closed';
        }
        
        // Update last update time
        document.getElementById('lastUpdate').textContent = data.last_updated.split(' ')[1];
        
    } catch (error) {
        console.error('Failed to update realtime price:', error);
    }
}

// Load stock data from API
async function loadStockData(symbol, timeframe = '1M') {
    try {
        // Default to 1M if no timeframe provided
        if (!timeframe) timeframe = '1M';
        
        const response = await fetch(`/api/stock/${symbol}?period=${timeframe}`);
        const data = await response.json();
        
        if (data.error) {
            console.error('Error loading stock data:', data.error);
            return;
        }
        
        updateStockDisplay(data);
        updateChart(data.historical, data.prediction);
        updatePrediction(data.prediction);
        updateStatistics();
        
        // Start real-time price updates (every second)
        startRealtimePriceUpdates(symbol);
        
    } catch (error) {
        console.error('Failed to load stock data:', error);
    }
}

// Update stock display
function updateStockDisplay(data) {
    document.getElementById('stockSymbol').textContent = data.symbol;
    document.getElementById('stockName').textContent = data.name;
    document.getElementById('stockExchange').textContent = data.exchange;
    
    const priceElement = document.getElementById('stockPrice');
    const changeElement = document.getElementById('stockChange');
    
    priceElement.textContent = data.current_price_formatted || `$${data.current_price.toFixed(2)}`;
    
    // Calculate change from historical data
    if (data.historical && data.historical.length > 1) {
        const firstPrice = data.historical[0].close;
        const lastPrice = data.historical[data.historical.length - 1].close;
        const changePercent = ((lastPrice - firstPrice) / firstPrice * 100);
        const changeSign = changePercent >= 0 ? '+' : '';
        
        changeElement.textContent = changeSign + changePercent.toFixed(2) + '%';
        changeElement.className = 'stock-change' + (changePercent < 0 ? ' negative' : '');
    }
}

// Update price chart
function updateChart(historical, prediction) {
    const ctx = document.getElementById('priceChart').getContext('2d');
    
    if (!historical || historical.length === 0) return;
    
    const labels = historical.map(d => d.date.slice(5));
    const prices = historical.map(d => d.close);
    
    // Add prediction points
    if (prediction && prediction.predictions) {
        const lastDate = new Date(historical[historical.length - 1].date);
        prediction.predictions.forEach((pred, i) => {
            const predDate = new Date(lastDate);
            predDate.setDate(predDate.getDate() + i + 1);
            labels.push(predDate.toISOString().slice(5, 10));
            prices.push(pred.predicted_price);
        });
    }
    
    if (priceChart) {
        priceChart.destroy();
    }
    
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(0, 255, 136, 0.3)');
    gradient.addColorStop(1, 'rgba(0, 255, 136, 0)');
    
    const predGradient = ctx.createLinearGradient(0, 0, 0, 300);
    predGradient.addColorStop(0, 'rgba(0, 212, 255, 0.3)');
    predGradient.addColorStop(1, 'rgba(0, 212, 255, 0)');
    
    const histLength = historical.length;
    
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Historical Price',
                    data: prices.slice(0, histLength),
                    borderColor: '#00ff88',
                    backgroundColor: gradient,
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    pointHoverBackgroundColor: '#00ff88'
                },
                {
                    label: 'AI Prediction',
                    data: [...Array(histLength - 1).fill(null), prices[histLength - 1], ...prices.slice(histLength)],
                    borderColor: '#00d4ff',
                    backgroundColor: predGradient,
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    pointHoverBackgroundColor: '#00d4ff'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        color: '#8b949e',
                        font: { family: 'Rajdhani' },
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(20, 27, 45, 0.9)',
                    titleColor: '#e8eaed',
                    bodyColor: '#e8eaed',
                    borderColor: '#1e3a5f',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': $' + context.parsed.y.toFixed(2);
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(30, 58, 95, 0.3)', drawBorder: false },
                    ticks: {
                        color: '#8b949e',
                        font: { family: 'JetBrains Mono', size: 10 },
                        maxRotation: 45
                    }
                },
                y: {
                    grid: { color: 'rgba(30, 58, 95, 0.3)', drawBorder: false },
                    ticks: {
                        color: '#8b949e',
                        font: { family: 'JetBrains Mono', size: 10 },
                        callback: function(value) { return '$' + value.toFixed(0); }
                    }
                }
            }
        }
    });
}

// Update prediction gauge
function updatePrediction(prediction) {
    if (!prediction) return;
    
    const probUp = prediction.probability_up || 50;
    const probDown = prediction.probability_down || 50;
    
    const gaugeNeedle = document.getElementById('gaugeNeedle');
    const gaugeFill = document.getElementById('gaugeFill');
    
    const angle = (probUp / 100) * 180 - 180;
    const radians = angle * Math.PI / 180;
    const needleLength = 70;
    const needleX = 100 + needleLength * Math.cos(radians);
    const needleY = 100 + needleLength * Math.sin(radians);
    
    gaugeNeedle.setAttribute('cx', needleX);
    gaugeNeedle.setAttribute('cy', needleY);
    
    const circumference = 251.2;
    const offset = circumference - (probUp / 100) * circumference;
    gaugeFill.style.strokeDashoffset = offset;
    
    document.getElementById('probUp').textContent = probUp;
    document.getElementById('probDownBar').style.width = probDown + '%';
    document.getElementById('probUpBar').style.width = probUp + '%';
    document.getElementById('probDown').textContent = probDown + '%';
    document.getElementById('probUpValue').textContent = probUp + '%';
    
    if (prediction.factors) {
        const factors = prediction.factors;
        document.getElementById('factorWar').textContent = (factors.war_impact * 100).toFixed(1) + '%';
        document.getElementById('factorTech').textContent = (factors.tech_impact * 100).toFixed(1) + '%';
        document.getElementById('factorResource').textContent = (factors.resource_impact * 100).toFixed(1) + '%';
        document.getElementById('factorNatural').textContent = (factors.natural_impact * 100).toFixed(1) + '%';
        
        ['factorWar', 'factorTech', 'factorResource', 'factorNatural'].forEach(id => {
            const el = document.getElementById(id);
            const value = parseFloat(el.textContent);
            el.className = 'factor-impact ' + (value >= 0 ? 'positive' : 'negative');
        });
    }
    
    const timelineContainer = document.getElementById('predictionTimeline');
    timelineContainer.innerHTML = '';
    
    if (prediction.predictions) {
        prediction.predictions.forEach(pred => {
            const item = document.createElement('div');
            item.className = 'timeline-item';
            item.innerHTML = `
                <div class="timeline-day">Day ${pred.day}</div>
                <div class="timeline-price">$${pred.predicted_price.toFixed(2)}</div>
                <div class="timeline-direction ${pred.direction}">${pred.direction === 'up' ? '▲' : '▼'}</div>
            `;
            timelineContainer.appendChild(item);
        });
    }
}

// Update statistics
async function updateStatistics() {
    try {
        const response = await fetch('/api/market/sentiment');
        const data = await response.json();
        
        document.getElementById('volatility').textContent = data.volatility_index;
        document.getElementById('volatilityBar').style.width = (data.volatility_index / 40 * 100) + '%';
        
        document.getElementById('sentiment').textContent = data.interpretation.charAt(0).toUpperCase() + data.interpretation.slice(1);
        document.getElementById('sentimentBar').style.width = data.overall_sentiment + '%';
        
        document.getElementById('confidence').textContent = Math.round(70 + Math.random() * 20) + '%';
        document.getElementById('confidenceBar').style.width = document.getElementById('confidence').textContent;
        
        document.getElementById('spChange').textContent = (data.sp500_change >= 0 ? '+' : '') + data.sp500_change.toFixed(2) + '%';
        
    } catch (error) {
        console.error('Failed to load sentiment:', error);
    }
}

// Load all events
async function loadAllEvents() {
    try {
        const response = await fetch('/api/events/all');
        const events = await response.json();
        
        renderWarEvents(events.war);
        renderTechEvents(events.tech);
        renderResourceEvents(events.resources);
        renderNaturalEvents(events.natural);
        
    } catch (error) {
        console.error('Failed to load events:', error);
    }
}

// Render events functions
function renderWarEvents(events) {
    const container = document.getElementById('warEventsList');
    container.innerHTML = '';
    events.forEach(event => {
        const item = document.createElement('div');
        item.className = 'event-item';
        item.innerHTML = `
            <div class="event-title">${event.title}</div>
            <div class="event-meta">
                <span>${event.location}</span>
                <div class="event-intensity">
                    <span>${(event.intensity * 100).toFixed(0)}%</span>
                    <div class="intensity-bar">
                        <div class="intensity-fill" style="width: ${event.intensity * 100}%"></div>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(item);
    });
    document.getElementById('warCount').textContent = events.length;
}

function renderTechEvents(events) {
    const container = document.getElementById('techEventsList');
    container.innerHTML = '';
    events.forEach(event => {
        const item = document.createElement('div');
        item.className = 'event-item';
        const impactClass = event.impact === 'positive' ? 'positive' : 'negative';
        const impactIcon = event.impact === 'positive' ? '↑' : '↓';
        
        item.innerHTML = `
            <div class="event-title">${event.title}</div>
            <div class="event-meta">
                <span>${event.category}</span>
                <div class="event-intensity">
                    <span class="${impactClass}">${impactIcon} ${(event.intensity * 100).toFixed(0)}%</span>
                </div>
            </div>
        `;
        container.appendChild(item);
    });
    document.getElementById('techCount').textContent = events.length;
}

function renderResourceEvents(resources) {
    const container = document.getElementById('resourceEventsList');
    container.innerHTML = '';
    resources.forEach(resource => {
        const item = document.createElement('div');
        item.className = 'resource-item';
        const shortagePercent = (resource.shortage_level * 100).toFixed(0);
        
        item.innerHTML = `
            <div>
                <div class="resource-name">${resource.name}</div>
                <div class="resource-level">${shortagePercent}% shortage</div>
            </div>
            <span class="resource-trend ${resource.trend}">${resource.trend}</span>
        `;
        container.appendChild(item);
    });
    document.getElementById('resourceCount').textContent = resources.length;
}

function renderNaturalEvents(events) {
    const container = document.getElementById('naturalEventsList');
    container.innerHTML = '';
    events.forEach(event => {
        const item = document.createElement('div');
        item.className = 'event-item';
        
        item.innerHTML = `
            <div class="event-title">${event.title}</div>
            <div class="event-meta">
                <span>${event.location}</span>
                <div class="event-intensity">
                    <span>${event.type}</span>
                    <div class="intensity-bar">
                        <div class="intensity-fill" style="width: ${event.severity * 100}%"></div>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(item);
    });
    document.getElementById('naturalCount').textContent = events.length;
}

// Load Chart.js
const chartJSScript = document.createElement('script');
chartJSScript.src = 'https://cdn.jsdelivr.net/npm/chart.js';
chartJSScript.onload = () => { console.log('Chart.js loaded'); };
document.head.appendChild(chartJSScript);

