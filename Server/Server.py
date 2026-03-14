"""
Basic Flask server for Catan game
No game logic - just the server infrastructure
"""
import sys
sys.path.append('/home/aakashlinux/Desktop/VirtualGame/CatanGame')
sys.path.append('/home/aakashlinux/Desktop/VirtualGame')
from Board import Board
from Tile import Tile
import uuid  # For generating unique game IDs
from flask import Flask, render_template, jsonify
from flask_cors import CORS
games = {}
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Home route
@app.route('/')
def create_game():
    # Generate unique game ID
    game_id = str(uuid.uuid4())
    

    # TO DO. Make a JSON file that contains nodes, tiles and edges
    

    # Create new Board instance
    board = Board()
    
    # Store it in the games dictionary
    games[game_id] = board
    
    # Return the game_id to the client
    return jsonify({
        'game_id': game_id,
        'message': 'Game created successfully'
    })

@app.route('/api/game/<game_id>/exists', methods=['GET'])
def game_exists(game_id):
    if game_id in games:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False}), 404


def index():
    """Main page"""
    return render_template('index.html')

# API route to check server status
@app.route('/api/status')
def status():
    """Check if server is running"""
    return jsonify({
        'status': 'online',
        'message': 'Catan server is running'
    })

# API route to get a test message
@app.route('/api/hello')
def hello():
    """Test endpoint"""
    return jsonify({
        'message': 'Hello from Catan server!'
    })

if __name__ == '__main__':
    print("=" * 60)
    print("CATAN GAME SERVER")
    print("=" * 60)
    print("\n🚀 Starting server...")
    print("📡 Server will be running at: http://localhost:5000")
    print("🛑 Press CTRL+C to stop the server\n")
    print("=" * 60)
    
    # Run the server
    app.run(
        host='0.0.0.0',  # Listen on all network interfaces
        port=5000,        # Port number
        debug=True        # Enable debug mode (auto-reload on code changes)
    )