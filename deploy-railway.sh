#!/bin/bash
# Automated Railway deployment script
# Run this after Railway login

echo "🚀 Deploying Survey Platform to Railway..."
echo ""

cd ~/survey-project

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    npm i -g @railway/cli
fi

echo "✅ Railway CLI ready"
echo ""
echo "Next steps:"
echo "1. Run: railway login"
echo "2. Run: railway init"
echo "3. Run: railway up"
echo "4. Run: railway domain"
echo ""
echo "Copy the domain URL and send to me for DNS setup!"
