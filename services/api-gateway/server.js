const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors({
  origin: [
    'https://logichain-frontend.vercel.app',
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:8081'   // <-- allow local React dev server
  ],
  credentials: true
}));
app.use(express.json());

// Service URLs
const SERVICES = {
  ROUTE_ENGINE: process.env.ROUTE_ENGINE_URL || 'https://logichain-route-engine.onrender.com'
};

// Rate limiting
const rateLimitMap = new Map();
const RATE_LIMIT = 100; // requests per minute

const rateLimiter = (req, res, next) => {
  const ip = req.ip;
  const now = Date.now();
  const windowStart = now - 60000; // 1 minute window
  
  if (!rateLimitMap.has(ip)) {
    rateLimitMap.set(ip, []);
  }
  
  const requests = rateLimitMap.get(ip);
  const recentRequests = requests.filter(time => time > windowStart);
  
  if (recentRequests.length >= RATE_LIMIT) {
    return res.status(429).json({ error: 'Rate limit exceeded' });
  }
  
  recentRequests.push(now);
  rateLimitMap.set(ip, recentRequests);
  next();
};

app.use(rateLimiter);

// Proxy function
const proxyRequest = async (req, res, serviceUrl) => {
  try {
    const response = await axios({
      method: req.method,
      url: `${serviceUrl}${req.path}`,
      data: req.body,
      headers: {
        'Content-Type': 'application/json',
        ...req.headers
      },
      timeout: 30000
    });
    
    res.status(response.status).json(response.data);
  } catch (error) {
    console.error(`Proxy error for ${serviceUrl}:`, error.message);
    
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
      res.status(503).json({ 
        error: 'Service temporarily unavailable',
        service: serviceUrl 
      });
    }
  }
};

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    service: 'api-gateway',
    timestamp: new Date().toISOString(),
    services: SERVICES
  });
});

// Route engine routes
app.use('/api/routes', (req, res) => {
  proxyRequest(req, res, SERVICES.ROUTE_ENGINE);
});

// Demo endpoints for testing
app.get('/api/demo/orders', (req, res) => {
  res.json([
    {
      id: '1',
      user_id: 1,
      items: [{ name: 'Package A', quantity: 2, weight: 5 }],
      delivery_address: { 
        street: '123 Main St', 
        city: 'New York', 
        latitude: 40.7128, 
        longitude: -74.0060 
      },
      status: 'pending',
      created_at: new Date().toISOString()
    },
    {
      id: '2',
      user_id: 1,
      items: [{ name: 'Package B', quantity: 1, weight: 3 }],
      delivery_address: { 
        street: '456 Oak Ave', 
        city: 'New York', 
        latitude: 40.7589, 
        longitude: -73.9851 
      },
      status: 'pending',
      created_at: new Date().toISOString()
    }
  ]);
});

app.post('/api/demo/routes/optimize', (req, res) => {
  const { stops } = req.body;
  
  // Simulate Dijkstra algorithm result
  res.json({
    routes: [[0, 1, 2, 0]],
    total_distance: stops ? stops.length * 5 : 25,
    estimated_time: stops ? stops.length * 8 : 45,
    algorithm: 'dijkstra',
    optimized: true
  });
});

// Error handling
app.use((error, req, res, next) => {
  console.error('API Gateway Error:', error);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, () => {
  console.log(`🚀 LogiChain API Gateway running on port ${PORT}`);
  console.log('📊 Services:', SERVICES);
});
