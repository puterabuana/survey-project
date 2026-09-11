#!/bin/bash
echo "🚀 Survey Platform Deployment Script"
echo ""
echo "Choose deployment platform:"
echo "1. Railway.app (recommended)"
echo "2. Render.com"
echo "3. Test locally only"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
  1)
    echo "📦 Deploying to Railway..."
    if ! command -v railway &> /dev/null; then
      echo "Installing Railway CLI..."
      npm i -g @railway/cli
    fi
    railway login
    railway init
    railway up
    echo ""
    echo "✅ Deployed! Get your URL:"
    railway domain
    ;;
  2)
    echo "📦 Preparing for Render.com..."
    echo "Steps:"
    echo "1. Push code to GitHub"
    echo "2. Go to render.com → New Web Service"
    echo "3. Connect GitHub repo"
    echo "4. Deploy"
    echo ""
    read -p "Initialize git and push to GitHub? (y/n): " git_choice
    if [ "$git_choice" = "y" ]; then
      git init
      git add .
      git commit -m "Survey research platform"
      echo "Now create a repo on GitHub and run:"
      echo "git remote add origin https://github.com/YOUR_USERNAME/survey-research.git"
      echo "git push -u origin main"
    fi
    ;;
  3)
    echo "🧪 Starting local server..."
    python3 app.py
    ;;
  *)
    echo "Invalid choice"
    ;;
esac
