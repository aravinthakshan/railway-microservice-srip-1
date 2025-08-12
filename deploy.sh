#!/bin/bash

# Railway Deployment Script for Rainfall PDF Parser Microservice

set -e

echo "🚀 Deploying Rainfall PDF Parser to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "Please login to Railway..."
    railway login
fi

# Check if project is initialized
if [ ! -f ".railway" ]; then
    echo "Initializing Railway project..."
    railway init
fi

# Deploy to Railway
echo "Deploying to Railway..."
railway up

# Get service status
echo "Service Status:"
railway status

# Get service URL
echo "Service URL:"
railway domain

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🔧 Next steps:"
echo "1. Test your service: curl https://your-service.railway.app/health"
echo "2. Update your Vercel app to call this service"
echo "3. Monitor logs: railway logs"
echo ""
echo "🎯 Your microservice is now running on Railway!" 