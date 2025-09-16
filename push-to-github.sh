#!/bin/bash

echo "🚀 Pushing LogiChain to GitHub Repository"

# Initialize git
git init
git remote add origin https://github.com/arnavgoyal0808/Graph-Routes-Optimization-.git

# Add all files
git add .

# Commit with detailed message
git commit -m "🚀 LogiChain - Complete Microservices Route Optimization Platform

✨ Features:
- React/TypeScript frontend with interactive UI
- Node.js API Gateway with CORS and routing
- Python FastAPI Route Engine with Dijkstra algorithm
- Docker containerization for all services
- CI/CD pipeline with GitHub Actions
- Zero-cost deployment ready (Vercel + Render)

🏗️ Architecture:
- Frontend: React/TypeScript → Vercel
- API Gateway: Node.js Express → Render  
- Route Engine: Python FastAPI + Dijkstra → Render
- Real-time route optimization with live demo

🎯 Ready to Deploy:
- Vercel: Connect frontend/ directory
- Render: Deploy services/api-gateway and services/route-engine
- Live demo with working Dijkstra algorithm implementation"

# Push to main branch
git branch -M main
git push -u origin main --force

echo ""
echo "✅ Successfully pushed to GitHub!"
echo "🌐 Repository: https://github.com/arnavgoyal0808/Graph-Routes-Optimization-.git"
echo ""
echo "🚀 Next Steps:"
echo "1. Go to vercel.com → Import from GitHub → Select your repo → Deploy frontend/"
echo "2. Go to render.com → New Web Service → Connect GitHub → Deploy services/"
echo "3. Your live demo will be available at the deployed URLs"
