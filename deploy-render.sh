#!/bin/bash

# Render Deployment Script for Rainfall PDF Parser Microservice

set -e

echo "🚀 Deploying Rainfall PDF Parser to Render..."

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please run this from your project root."
    exit 1
fi

# Check if there are uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 You have uncommitted changes. Committing them..."
    git add .
    git commit -m "Update rainfall PDF parser microservice for Render deployment"
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Code pushed to GitHub!"
echo ""
echo "🌐 Now deploy to Render:"
echo "1. Go to https://render.com and sign up/login"
echo "2. Click 'New +' → 'Web Service'"
echo "3. Connect your GitHub repository"
echo "4. Select the 'railway-microservice' folder"
echo "5. Configure:"
echo "   - Name: rainfall-pdf-parser"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: python main.py"
echo "6. Click 'Create Web Service'"
echo ""
echo "🎯 Render will automatically deploy from your GitHub repository!"
echo "📊 Monitor deployment in the Render dashboard"
echo "🔗 Your service will be available at: https://your-service.onrender.com" 