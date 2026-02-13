from flask import Flask, render_template, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

# Import your Board class
# Assuming your Board.py is in a package, adjust the import accordingly
# from your_package.Board import Board

# For now, we'll create a mock board data structure
# Replace this with: board = Board() once you import it
board = None

@app.route('/')
def index():
    return render_template('board.html')

@app.route('/api/board')
def get_board_data():
    """Convert board state to JSON for frontend rendering"""
    
    # If you have a real board instance, use this:
    # if board is None:
    #     board = Board()
    
    # For now, returning structure - replace with actual board data
    board_data = {
        'tiles': [],
        'nodes': [],
        'edges': []
    }
    
    # If you have the board instance, extract data like this:
    if board is not None:
        # Extract tile information
        tile_layout = [
            [0, 1, 2],
            [3, 4, 5, 6],
            [7, 8, 9, 10, 11],
            [12, 13, 14, 15],
            [16, 17, 18]
        ]
        
        hex_width = 2.0
        hex_height = 1.732
        
        tiles_data = []
        for row_idx, row in enumerate(tile_layout):
            y = -row_idx * hex_height * 0.75
            x_offset = -(len(row) - 1) * hex_width / 2
            
            for col_idx, tile_idx in enumerate(row):
                tile = board.tiles[tile_idx]
                center_x = x_offset + col_idx * hex_width
                center_y = y
                
                tiles_data.append({
                    'id': tile_idx,
                    'resource': tile.resource,
                    'number': tile.number,
                    'center_x': center_x,
                    'center_y': center_y
                })
        
        board_data['tiles'] = tiles_data
        
        # Extract node positions and data
        node_positions = create_hex_positions(board.tiles)
        nodes_data = []
        node_id_map = {}
        
        for idx, (node, pos) in enumerate(node_positions.items()):
            node_id_map[id(node)] = idx
            nodes_data.append({
                'id': idx,
                'x': pos[0],
                'y': pos[1],
                'resources': node.resources,
                'numbers': node.numbers
            })
        
        board_data['nodes'] = nodes_data
        
        # Extract edges
        edges_data = []
        for edge in board.G.edges():
            node1_id = node_id_map.get(id(edge[0]))
            node2_id = node_id_map.get(id(edge[1]))
            if node1_id is not None and node2_id is not None:
                edges_data.append({
                    'source': node1_id,
                    'target': node2_id
                })
        
        board_data['edges'] = edges_data
    
    return jsonify(board_data)

def create_hex_positions(tiles):
    """Create positions for nodes around hexagonal tiles"""
    pos = {}
    
    tile_layout = [
        [0, 1, 2],
        [3, 4, 5, 6],
        [7, 8, 9, 10, 11],
        [12, 13, 14, 15],
        [16, 17, 18]
    ]
    
    hex_width = 2.0
    hex_height = 1.732
    
    for row_idx, row in enumerate(tile_layout):
        y = -row_idx * hex_height * 0.75
        x_offset = -(len(row) - 1) * hex_width / 2
        
        for col_idx, tile_idx in enumerate(row):
            tile = tiles[tile_idx]
            center_x = x_offset + col_idx * hex_width
            center_y = y
            
            for node_idx, node in enumerate(tile.nodes):
                angle = math.pi / 3 * node_idx - math.pi / 2
                node_x = center_x + 0.5 * math.cos(angle)
                node_y = center_y + 0.5 * math.sin(angle)
                
                if node not in pos:
                    pos[node] = (node_x, node_y)
    
    return pos

if __name__ == '__main__':
    # Uncomment this when you have Board imported:
    # board = Board()
    print("Starting Catan Board Server...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
