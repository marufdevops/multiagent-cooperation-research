"""
Launch Solara visualization server.
Run with: python scripts/run_visualization.py
Then open browser to http://localhost:8765
"""
import os
import subprocess

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Solara Visualization Server")
    print("=" * 60)
    print("Open your browser to: http://localhost:8765")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    # Set PYTHONPATH to include src directory
    env = os.environ.copy()
    current_path = env.get('PYTHONPATH', '')
    src_path = os.path.join(os.getcwd(), 'src')
    env['PYTHONPATH'] = f"{src_path}:{current_path}" if current_path else src_path

    # Run solara with the visualization module
    try:
        subprocess.run(
            ['/opt/anaconda3/bin/solara', 'run', 'src/visualization/solara_viz.py', '--port', '8765'],
            env=env,
            check=True
        )
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("Server stopped")
        print("=" * 60)
    except subprocess.CalledProcessError as e:
        print(f"\nError running Solara: {e}")
        print("\nAlternative: Run directly with:")
        print("  cd src/visualization && /opt/anaconda3/bin/solara run solara_viz.py --port 8765")

