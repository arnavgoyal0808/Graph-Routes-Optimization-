# LogiChain - Graph Routes Optimization Platform

🚀 **Live Demo**: [Frontend](https://logichain-frontend.vercel.app) | [API](https://logichain-api.onrender.com)

## Overview
LogiChain is a production-ready microservices platform that solves the Multi-Stop Vehicle Routing Problem using Dijkstra's algorithm and real street network data from OpenStreetMap.

## Architecture
- **Frontend**: React/TypeScript (Vercel)
- **API Gateway**: Node.js Express (Render)
- **Route Engine**: Python FastAPI + Dijkstra Algorithm (Render)
- **Databases**: PostgreSQL (Neon.tech) + MongoDB Atlas
- **Cache**: Redis (Render)
- **Queue**: RabbitMQ (CloudAMQP)

## Quick Start

### 1. Local Development
```bash
./scripts/setup.sh
docker-compose up
```

### 2. Deploy to Production
- Frontend → Vercel (connect GitHub repo, set root: `frontend`)
- API Gateway → Render (deploy `services/api-gateway`)
- Route Engine → Render (deploy `services/route-engine`)

## Features
- 🗺️ Real-time route optimization using Dijkstra's algorithm
- 📱 Responsive React dashboard
- 🔄 Microservices architecture with polyglot persistence
- 🚀 Zero-cost deployment on free tiers
- 📊 Live monitoring and health checks

## API Endpoints
- `GET /health` - Service health check
- `POST /api/routes/optimize` - Route optimization
- `POST /api/orders` - Create delivery order
- `GET /api/users/profile` - User profile

## Technology Stack
- **Frontend**: React 18, TypeScript, Tailwind CSS
- **Backend**: Node.js, Python FastAPI
- **Algorithms**: Dijkstra, Route Optimization
- **Databases**: PostgreSQL, MongoDB, Redis
- **Deployment**: Vercel, Render, Docker
- **CI/CD**: GitHub Actions

## Contributing
1. Fork the repository
2. Create feature branch
3. Make changes
4. Run tests: `npm test`
5. Submit pull request

## License
MIT License - see [LICENSE](LICENSE) file
