#!/bin/bash

echo "🐳 Building Vector DB Docker Image..."

# Build the main API image
docker build -t vector-db-api:latest .

echo "✅ Build complete!"
echo ""
echo "🚀 To run the container:"
echo "  docker run -p 8000:8000 -v \$(pwd)/db.json:/app/db.json vector-db-api:latest"
echo ""
echo "🔗 Or use docker-compose:"
echo "  docker-compose up"
echo ""
echo "📱 To include the Streamlit UI:"
echo "  docker-compose --profile ui up"
