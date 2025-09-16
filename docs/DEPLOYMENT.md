# LogiChain Deployment Guide

## Live Architecture Overview

LogiChain is deployed using a microservices architecture with the following live services:

### Production Services
- **Frontend**: React app deployed on Vercel
- **API Gateway**: Node.js service on Render
- **Route Engine**: Python FastAPI service on Render
- **Databases**: PostgreSQL (Neon.tech) + MongoDB Atlas
- **Cache**: Redis on Render
- **Queue**: RabbitMQ on CloudAMQP

## Deployment Steps

### 1. Prerequisites
- GitHub account
- Vercel account (free)
- Render account (free)
- Neon.tech account (free)
- MongoDB Atlas account (free)

### 2. Fork and Clone Repository
```bash
git clone https://github.com/arnavgoyal0808/Graph-Routes-Optimization-.git
cd Graph-Routes-Optimization-
```

### 3. Deploy Frontend (Vercel)
1. Connect GitHub repo to Vercel
2. Set build command: `npm run build`
3. Set output directory: `build`
4. Add environment variable: `REACT_APP_API_URL=https://your-api-gateway.onrender.com/api`
5. Deploy automatically on push to main

### 4. Deploy API Gateway (Render)
1. Create new Web Service on Render
2. Connect GitHub repo
3. Set build command: `cd services/api-gateway && npm install`
4. Set start command: `cd services/api-gateway && npm start`
5. Add environment variables:
   - `ROUTE_ENGINE_URL=https://your-route-engine.onrender.com`

### 5. Deploy Route Engine (Render)
1. Create new Web Service on Render
2. Connect GitHub repo
3. Set build command: `cd services/route-engine && pip install -r requirements.txt`
4. Set start command: `cd services/route-engine && python main.py`

### 6. Set up Databases
#### PostgreSQL (Neon.tech)
1. Create database at https://neon.tech
2. Copy connection string
3. Add to Render environment variables

#### MongoDB Atlas
1. Create cluster at https://cloud.mongodb.com
2. Create database user
3. Copy connection string
4. Add to Render environment variables

### 7. Configure CI/CD
1. Add secrets to GitHub repository:
   - `VERCEL_TOKEN`
   - `VERCEL_ORG_ID`
   - `VERCEL_PROJECT_ID`
   - `RENDER_API_KEY`
   - `RENDER_API_GATEWAY_SERVICE_ID`
   - `RENDER_ROUTE_ENGINE_SERVICE_ID`

## Environment Variables

### Frontend (.env)
```
REACT_APP_API_URL=https://logichain-api.onrender.com/api
```

### API Gateway
```
PORT=3000
ROUTE_ENGINE_URL=https://logichain-route-engine.onrender.com
USER_SERVICE_URL=https://logichain-user-service.onrender.com
ORDER_SERVICE_URL=https://logichain-order-service.onrender.com
```

### Route Engine
```
PORT=8001
```

## Monitoring and Health Checks

### Health Endpoints
- API Gateway: `GET /health`
- Route Engine: `GET /health`

### Monitoring Setup
1. Sign up for Better Stack (free)
2. Add uptime monitoring for all services
3. Set up alerts for downtime

## Cost Optimization

### Free Tier Limits
- **Vercel**: Unlimited static deployments
- **Render**: 750 hours/month (sufficient for 2-3 services)
- **Neon.tech**: 0.5GB PostgreSQL storage
- **MongoDB Atlas**: 512MB storage
- **Better Stack**: Basic monitoring

### Optimization Tips
1. Use efficient Docker images
2. Implement proper caching
3. Optimize database queries
4. Use connection pooling
5. Monitor resource usage

## Troubleshooting

### Common Issues
1. **Service not responding**: Check Render logs
2. **CORS errors**: Verify frontend URL in API Gateway
3. **Database connection**: Check connection strings
4. **Build failures**: Verify dependencies and build commands

### Debug Commands
```bash
# Check service logs
curl https://your-service.onrender.com/health

# Local testing
docker-compose up
curl http://localhost:3000/health
curl http://localhost:8001/health
```

## Scaling Considerations

### Horizontal Scaling
- Add more Render services
- Use load balancers
- Implement service discovery

### Performance Optimization
- Add Redis caching
- Optimize algorithms
- Use CDN for static assets
- Implement database indexing

This deployment guide ensures a production-ready, scalable LogiChain platform with zero hosting costs.
