#!/bin/bash

echo "🚀 Deploying Solution Tree Virtual Coach to Firebase..."
echo ""
echo "Note: Make sure you're logged in as miriam.rose.simone@gmail.com"
echo ""

# Build the app
echo "📦 Building production bundle..."
npm run build

if [ $? -ne 0 ]; then
  echo "❌ Build failed!"
  exit 1
fi

echo ""
echo "✅ Build successful!"
echo ""
echo "🔐 Deploying to Firebase..."
echo "If you see authentication errors, run: firebase login"
echo ""

# Deploy to Firebase
firebase deploy --only hosting

if [ $? -eq 0 ]; then
  echo ""
  echo "✅ Deployment successful!"
  echo "🌐 Your app is live at: https://solutiontreevirtualcoach.web.app"
else
  echo ""
  echo "❌ Deployment failed!"
  echo "Try running: firebase login"
  exit 1
fi
