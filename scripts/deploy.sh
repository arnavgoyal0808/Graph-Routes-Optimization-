#!/bin/bash

echo "🚀 Deploying LogiChain to Production"

# Check if required environment variables are set
if [ -z "$VERCEL_TOKEN" ]; then
    echo "❌ VERCEL_TOKEN environment variable is not set"
    echo "   Get your token from: https://vercel.com/account/tokens"
    exit 1
fi

if [ -z "$RENDER_API_KEY" ]; then
    echo "❌ RENDER_API_KEY environment variable is not set"
    echo "   Get your API key from: https://dashboard.render.com/account/api-keys"
    exit 1
fi

echo "✅ Environment variables are set"

# Deploy Frontend to Vercel
echo "📱 Deploying Frontend to Vercel..."
cd frontend
npx vercel --prod --token $VERCEL_TOKEN
cd ..

# Deploy API Gateway to Render
echo "🌐 Deploying API Gateway to Render..."
if [ ! -z "$RENDER_API_GATEWAY_SERVICE_ID" ]; then
    curl -X POST \
        -H "Authorization: Bearer $RENDER_API_KEY" \
        -H "Content-Type: application/json" \
        "https://api.render.com/v1/services/$RENDER_API_GATEWAY_SERVICE_ID/deploys"
    echo "✅ API Gateway deployment triggered"
else
    echo "⚠️  RENDER_API_GATEWAY_SERVICE_ID not set, skipping API Gateway deployment"
fi

# Deploy Route Engine to Render
echo "🗺️  Deploying Route Engine to Render..."
if [ ! -z "$RENDER_ROUTE_ENGINE_SERVICE_ID" ]; then
    curl -X POST \
        -H "Authorization: Bearer $RENDER_API_KEY" \
        -H "Content-Type: application/json" \
        "https://api.render.com/v1/services/$RENDER_ROUTE_ENGINE_SERVICE_ID/deploys"
    echo "✅ Route Engine deployment triggered"
else
    echo "⚠️  RENDER_ROUTE_ENGINE_SERVICE_ID not set, skipping Route Engine deployment"
fi

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "🌐 Live URLs:"
echo "   Frontend: https://logichain-frontend.vercel.app"
echo "   API:      https://logichain-api.onrender.com"
echo ""
echo "📊 Monitor deployments:"
echo "   Vercel:   https://vercel.com/dashboard"
echo "   Render:   https://dashboard.render.com"
