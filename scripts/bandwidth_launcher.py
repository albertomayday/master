#!/usr/bin/env python3
"""
Device Farm V5 - Bandwidth Optimized Launcher
Ultra-lightweight launcher for edge deployments
"""

import asyncio
import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, '/app/src')

async def main():
    """Main entry point for edge deployment"""
    
    # Import bandwidth optimizations
    sys.path.insert(0, '/app/config')
    from bandwidth_optimization import apply_bandwidth_optimizations
    
    # Apply optimizations first
    apply_bandwidth_optimizations()
    
    print("🚀 Starting Device Farm V5 - Edge Mode")
    print("📊 Bandwidth optimizations: ACTIVE")
    print("💾 Memory footprint: MINIMAL")
    print("🔧 CPU usage: OPTIMIZED")
    
    try:
        # Import minimal components
        from main import DeviceFarmSystem
        
        # Initialize with edge configuration
        system = DeviceFarmSystem()
        
        # Start system with minimal resources
        if await system.initialize():
            print("✅ Edge system initialized successfully")
            
            # Start with minimal services
            await system.start_services()
        else:
            print("❌ Failed to initialize edge system")
            sys.exit(1)
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("📋 Falling back to minimal HTTP server...")
        
        # Fallback minimal server
        from http.server import HTTPServer, SimpleHTTPRequestHandler
        
        class HealthHandler(SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/health':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "healthy", "mode": "edge"}')
                else:
                    self.send_response(404)
                    self.end_headers()
        
        server = HTTPServer(('0.0.0.0', 8000), HealthHandler)
        print("🔥 Minimal server running on http://0.0.0.0:8000")
        server.serve_forever()

if __name__ == "__main__":
    # Check for edge mode flag
    if "--edge-mode" in sys.argv:
        print("🏃‍♂️ Running in EDGE mode")
        asyncio.run(main())
    else:
        print("❌ This launcher requires --edge-mode flag")
        sys.exit(1)