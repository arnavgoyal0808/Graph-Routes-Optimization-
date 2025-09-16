#!/bin/bash
echo "🚀 Setting up LogiChain"

cd frontend && npm install && cd ..
cd services/api-gateway && npm install && cd ../..

echo "✅ Dependencies installed"
echo "🐳 Starting services with Docker..."

docker-compose up --build -d

echo "🎉 LogiChain is running!"
echo "Frontend: http://localhost:3001"
echo "API Gateway: http://localhost:3000"
