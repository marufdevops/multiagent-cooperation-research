"""
Launch Solara visualization server.
Run with: python scripts/run_visualization.py
Then open browser to http://localhost:8765
"""
import sys
sys.path.insert(0, 'src')

from visualization.solara_viz import page

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Solara Visualization Server")
    print("=" * 60)
    print("Open your browser to: http://localhost:8765")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Solara will automatically serve the page
    import solara.server.starlette
    solara.server.starlette.run(page, port=8765)

