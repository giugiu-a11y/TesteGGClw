#!/bin/bash

# Pokémon Adventures Game - Dev Server

echo "🎮 Pokémon Adventures - Starting Dev Server"
echo "=========================================="
echo ""

cd /home/ubuntu/clawd/pokemon-game/

# Get local IP
LOCAL_IP=$(hostname -I | awk '{print $1}')

echo "📁 Directory: /home/ubuntu/clawd/pokemon-game/"
echo "🌐 Local Server: http://localhost:8000"
echo "📱 iPad Access: http://$LOCAL_IP:8000"
echo ""
echo "Open your iPad Safari and go to: http://$LOCAL_IP:8000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 -m http.server 8000 --bind 0.0.0.0
