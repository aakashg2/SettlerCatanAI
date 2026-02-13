#!/usr/bin/env python3
"""
Simple Catan Board Server - No Flask Required
Uses Python's built-in http.server module
"""

import http.server
import socketserver
import json
import math
from urllib.parse import urlparse, parse_qs

# Import your Board class here
# from Board import Board

PORT = 8000

class CatanBoardHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.serve_html()
        elif parsed_path.path == '/api/board':
            self.serve_board_data()
        else:
            super().do_GET()
    
    def serve_html(self):
        """Serve the board visualization HTML"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catan Board Viewer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 30px;
            max-width: 1200px;
        }
        h1 { text-align: center; color: #333; margin-bottom: 20px; }
        #boardCanvas {
            display: block;
            margin: 0 auto;
            border: 2px solid #333;
            border-radius: 10px;
            background: #f0e6d2;
            cursor: move;
        }
        .controls {
            margin-top: 20px;
            text-align: center;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 0 5px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover { background: #764ba2; }
        .info-panel {
            margin-top: 15px;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 8px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎲 Catan Board Viewer</h1>
        <canvas id="boardCanvas" width="1000" height="800"></canvas>
        <div class="controls">
            <button onclick="zoomIn()">Zoom In</button>
            <button onclick="zoomOut()">Zoom Out</button>
            <button onclick="resetView()">Reset</button>
            <button onclick="toggleNodes()">Toggle Nodes</button>
        </div>
        <div class="info-panel">
            <p id="infoText">Drag to pan, use buttons to zoom</p>
        </div>
    </div>
    
    <script>
        const canvas = document.getElementById('boardCanvas');
        const ctx = canvas.getContext('2d');
        
        let scale = 70;
        let offsetX = canvas.width / 2;
        let offsetY = canvas.height / 2 + 50;
        let showNodes = true;
        
        const resourceColors = {
            'rock': '#8B7355', 'mud': '#CD853F', 'wheat': '#F4A460',
            'tree': '#228B22', 'sheep': '#90EE90', 'desert': '#F5DEB3'
        };
        
        async function loadBoard() {
            try {
                const response = await fetch('/api/board');
                const boardData = await response.json();
                if (boardData.tiles.length > 0) {
                    drawBoardData(boardData);
                } else {
                    drawSampleBoard();
                }
            } catch (error) {
                console.error('Loading sample board:', error);
                drawSampleBoard();
            }
        }
        
        function drawBoardData(boardData) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            boardData.tiles.forEach(tile => {
                drawHexagon(tile.center_x, tile.center_y, tile.resource, tile.number);
            });
            
            if (showNodes && boardData.edges) {
                ctx.strokeStyle = '#8B4513';
                ctx.lineWidth = 2;
                boardData.edges.forEach(edge => {
                    const s = boardData.nodes[edge.source];
                    const t = boardData.nodes[edge.target];
                    if (s && t) {
                        ctx.beginPath();
                        ctx.moveTo(offsetX + s.x * scale, offsetY + s.y * scale);
                        ctx.lineTo(offsetX + t.x * scale, offsetY + t.y * scale);
                        ctx.stroke();
                    }
                });
            }
            
            if (showNodes && boardData.nodes) {
                boardData.nodes.forEach(node => {
                    drawNode(node.x, node.y, node.resources);
                });
            }
        }
        
        function drawSampleBoard() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const layout = [[0,1,2], [3,4,5,6], [7,8,9,10,11], [12,13,14,15], [16,17,18]];
            const res = ['rock','mud','wheat','tree','sheep','wheat','tree','mud','wheat',
                        'sheep','rock','tree','sheep','wheat','rock','sheep','mud','tree','desert'];
            const nums = [10,2,9,12,6,4,10,9,11,3,8,8,3,4,5,5,6,11,-1];
            
            layout.forEach((row, r) => {
                const y = -r * 1.732 * 0.75;
                const xOff = -(row.length - 1);
                row.forEach((idx, c) => {
                    drawHexagon(xOff + c * 2, y, res[idx], nums[idx]);
                });
            });
        }
        
        function drawHexagon(x, y, resource, number) {
            const sx = offsetX + x * scale;
            const sy = offsetY + y * scale;
            const r = 0.55 * scale;
            
            ctx.beginPath();
            for (let i = 0; i < 6; i++) {
                const a = Math.PI/3*i - Math.PI/2;
                const px = sx + r*Math.cos(a);
                const py = sy + r*Math.sin(a);
                i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
            }
            ctx.closePath();
            ctx.fillStyle = resourceColors[resource] || '#CCC';
            ctx.fill();
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 3;
            ctx.stroke();
            
            if (number > 0) {
                ctx.fillStyle = '#F5E6D3';
                ctx.beginPath();
                ctx.arc(sx, sy, r*0.4, 0, Math.PI*2);
                ctx.fill();
                ctx.stroke();
                
                ctx.fillStyle = (number===6||number===8) ? '#DC143C' : '#333';
                ctx.font = 'bold ' + (r*0.5) + 'px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(number, sx, sy);
            }
        }
        
        function drawNode(x, y, resources) {
            const sx = offsetX + x * scale;
            const sy = offsetY + y * scale;
            const colors = {1:'lightcoral', 2:'lightblue', 3:'lightgreen'};
            const color = resources ? (colors[resources.length] || 'gold') : 'lightcoral';
            
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(sx, sy, 8, 0, Math.PI*2);
            ctx.fill();
            ctx.strokeStyle = '#000';
            ctx.lineWidth = 2;
            ctx.stroke();
        }
        
        function zoomIn() { scale *= 1.2; loadBoard(); }
        function zoomOut() { scale /= 1.2; loadBoard(); }
        function resetView() { scale=70; offsetX=canvas.width/2; offsetY=canvas.height/2+50; loadBoard(); }
        function toggleNodes() { showNodes = !showNodes; loadBoard(); }
        
        let isDragging = false, lastX, lastY;
        canvas.addEventListener('mousedown', e => { isDragging=true; lastX=e.clientX; lastY=e.clientY; });
        canvas.addEventListener('mousemove', e => {
            if (isDragging) {
                offsetX += e.clientX - lastX;
                offsetY += e.clientY - lastY;
                lastX = e.clientX;
                lastY = e.clientY;
                loadBoard();
            }
        });
        canvas.addEventListener('mouseup', () => isDragging=false);
        canvas.addEventListener('mouseleave', () => isDragging=false);
        
        loadBoard();
    </script>
</body>
</html>
"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def serve_board_data(self):
        """Serve board data as JSON"""
        # For now, return empty structure
        # Uncomment and modify when you have Board imported
        
        board_data = {
            'tiles': [],
            'nodes': [],
            'edges': []
        }
        
        # Uncomment this section when Board is imported:
        """
        try:
            board = Board()
            board_data = extract_board_data(board)
        except Exception as e:
            print(f"Error creating board: {e}")
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(board_data).encode())

def extract_board_data(board):
    """Extract board data for JSON serialization"""
    tile_layout = [[0,1,2], [3,4,5,6], [7,8,9,10,11], [12,13,14,15], [16,17,18]]
    
    tiles_data = []
    hex_width = 2.0
    hex_height = 1.732
    
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
    
    # Extract nodes
    node_positions = {}
    for row_idx, row in enumerate(tile_layout):
        y = -row_idx * hex_height * 0.75
        x_offset = -(len(row) - 1) * hex_width / 2
        
        for col_idx, tile_idx in enumerate(row):
            tile = board.tiles[tile_idx]
            center_x = x_offset + col_idx * hex_width
            center_y = y
            
            for node_idx, node in enumerate(tile.nodes):
                angle = math.pi / 3 * node_idx - math.pi / 2
                node_x = center_x + 0.5 * math.cos(angle)
                node_y = center_y + 0.5 * math.sin(angle)
                
                if node not in node_positions:
                    node_positions[node] = (node_x, node_y)
    
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
    
    # Extract edges
    edges_data = []
    for edge in board.G.edges():
        n1_id = node_id_map.get(id(edge[0]))
        n2_id = node_id_map.get(id(edge[1]))
        if n1_id is not None and n2_id is not None:
            edges_data.append({'source': n1_id, 'target': n2_id})
    
    return {
        'tiles': tiles_data,
        'nodes': nodes_data,
        'edges': edges_data
    }

if __name__ == '__main__':
    # Uncomment to use your actual Board:
    # from Board import Board
    
    print(f"Starting Catan Board Server on port {PORT}")
    print(f"Open http://localhost:{PORT} in your browser")
    print("Press Ctrl+C to stop")
    
    with socketserver.TCPServer(("", PORT), CatanBoardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
