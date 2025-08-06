#!/bin/bash

echo "🚀 Deploying HackRx 6.0 to Render..."

# Check if render-cli is installed
if ! command -v render &> /dev/null; then
    echo "Installing Render CLI..."
    npm install -g @render-com/render-cli
fi

# Deploy to Render
echo "Deploying services..."
render deploy

echo "✅ Deployment completed! Check your Render dashboard for status."
