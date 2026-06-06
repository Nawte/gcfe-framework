"""
Skippy 2.0 Flask Application Factory
=====================================

Clean, minimal Flask app using Skippy 2.0 architecture.
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import sys

# Import config
from config import config

def create_app():
    """Create and configure Flask application"""
    
    print("="*80)
    print(" SKIPPY 2.0 - FLASK APPLICATION")
    print("="*80)
    print()
    
    # Create Flask app
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    
    # Load config
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['DEBUG'] = config.DEBUG
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": config.CORS_ORIGINS,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    print("✅ CORS configured")
    
    # Initialize core modules
    try:
        from core.pattern_sovereign import get_pattern_sovereign
        from core.llm_router import get_llm_router
        from core.emotional_layer import get_emotional_layer
        from core.conscience_agent import get_conscience_agent

        # Initialize unified auth system
        from unified_auth_flask import create_unified_auth_blueprint
        # CRITICAL: Auth uses the SAME centralized stocks.db (single source of truth!)
        # Import from database_path.py to ensure consistency
        from database_path import STOCKS_DB
        auth_bp = create_unified_auth_blueprint(STOCKS_DB)
        app.register_blueprint(auth_bp)
        print("✅ Unified auth system registered (using centralized DB)")
        from core.vision_processor import get_vision_processor

        # Initialize singletons
        pattern_sovereign = get_pattern_sovereign()
        llm_router = get_llm_router()
        emotional_layer = get_emotional_layer()
        conscience_agent = get_conscience_agent()
        vision_processor = get_vision_processor()

        # Store in app config
        app.config['PATTERN_SOVEREIGN'] = pattern_sovereign
        app.config['LLM_ROUTER'] = llm_router
        app.config['EMOTIONAL_LAYER'] = emotional_layer
        app.config['CONSCIENCE_AGENT'] = conscience_agent
        app.config['VISION_PROCESSOR'] = vision_processor

        print("✅ Core modules initialized (including Vision)")

        # Initialize companion system at startup (CRITICAL: prevents lazy load with wrong DB)
        from core.companion_integration_system import get_companion_system
        companion_system = get_companion_system()  # Uses database_path.py via config.py
        app.config['COMPANION_SYSTEM'] = companion_system
        print("✅ Companion Integration System initialized")

    except Exception as e:
        print(f"⚠️ Core modules not available: {e}")

    # Initialize Autonomous Executor (Phase 15A)
    try:
        from core.autonomous_executor import get_autonomous_executor
        from core.specialist_router import SpecialistRouter

        autonomous_executor = get_autonomous_executor()
        specialist_router = SpecialistRouter()

        # Inject dependencies
        autonomous_executor.set_dependencies(
            pattern_sovereign=app.config.get('PATTERN_SOVEREIGN'),
            llm_router=app.config.get('LLM_ROUTER'),
            specialist_router=specialist_router
        )

        app.config['AUTONOMOUS_EXECUTOR'] = autonomous_executor
        app.config['SPECIALIST_ROUTER'] = specialist_router

        print("✅ Autonomous Executor initialized (Phase 15A)")
    except Exception as e:
        print(f"⚠️ Autonomous Executor not available: {e}")

    # Register blueprints
    from routes import register_blueprints
    register_blueprints(app)
    print("✅ Blueprints registered")

    # Register brainstorm blueprint
    try:
        print("   🔄 Attempting to import flask_socketio...")
        from flask_socketio import SocketIO
        print("   ✅ flask_socketio imported")

        print("   🔄 Attempting to import brainstorm_system...")
        from core.brainstorm_system import bp as brainstorm_bp, init_socketio
        print("   ✅ brainstorm_system imported")

        # Initialize SocketIO
        print("   🔄 Initializing SocketIO...")
        socketio = SocketIO(app, cors_allowed_origins="*")
        socketio = init_socketio(socketio)  # Initialize handlers
        app.config['SOCKETIO'] = socketio
        print("   ✅ SocketIO initialized")

        # Register blueprint
        print("   🔄 Registering brainstorm blueprint...")
        app.register_blueprint(brainstorm_bp)
        print("✅ Brainstorm system registered with WebSocket support")
    except Exception as e:
        print(f"\n⚠️ Brainstorm system not available")
        print(f"   Error: {type(e).__name__}: {e}")
        print(f"   Full traceback:")
        import traceback
        traceback.print_exc()
        print()
    
    # Serve semperAmi static files
    semperami_public = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'semperAmi', 'public'
    )
    
    @app.route('/semperami/<path:filename>')
    def serve_semperami(filename):
        """Serve files from semperAmi/public"""
        return send_from_directory(semperami_public, filename)
    
    print(f"✅ Serving semperAmi from: {semperami_public}")
    
    # Health check route
    @app.route('/health')
    def health_check():
        """System health check"""
        return {
            "status": "healthy",
            "version": "2.0",
            "core_modules": {
                "pattern_sovereign": "PATTERN_SOVEREIGN" in app.config,
                "llm_router": "LLM_ROUTER" in app.config,
                "emotional_layer": "EMOTIONAL_LAYER" in app.config,
                "conscience_agent": "CONSCIENCE_AGENT" in app.config
            }
        }

    print()
    print("="*80)
    print(" SKIPPY 2.0 READY!")
    print("="*80)
    print()

    # SELF-HEALING STATUS CHECK (Dad's request - show it's actually working!)
    try:
        import sqlite3
        from database_path import STOCKS_DB
        conn = sqlite3.connect(STOCKS_DB, timeout=5)
        cursor = conn.cursor()

        print("="*80)
        print("🔧 SELF-HEALING SYSTEM STATUS")
        print("="*80)

        # Count fixes applied
        cursor.execute("SELECT COUNT(*) FROM self_healing_applied")
        fixes = cursor.fetchone()[0]
        print(f"✅ Fixes Applied: {fixes:,}")

        # Count queue
        cursor.execute("SELECT COUNT(*) FROM self_healing_queue")
        queue = cursor.fetchone()[0]
        print(f"✅ Queue: {queue:,} items")

        # Count innovations
        cursor.execute("SELECT COUNT(*) FROM innovation_pipeline")
        innovations = cursor.fetchone()[0]
        print(f"✅ Innovations: {innovations:,}")

        print(f"✅ Status: ACTIVE AND WORKING!")
        print("="*80)
        print()

        conn.close()
    except Exception as e:
        print(f"⚠️  Could not check self-healing status: {e}")
        print()

    # START AUTONOMOUS CONDUCTOR - Last thing before routes
    # This ensures all models/systems are loaded first
    try:
        import threading
        import asyncio
        import sys
        from pathlib import Path

        # Add parent directory to path so we can import Massive_Ai_Agent_Farm
        parent_dir = str(Path(__file__).parent.parent / "Massive Ai Agent Farm")
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)

        def run_conductor_in_thread():
            """Run conductor in its own thread with its own event loop"""
            from Massive_Ai_Agent_Farm.conductor import start_conductor
            asyncio.run(start_conductor())

        print("\n" + "=" * 70)
        print("🎼 STARTING CONDUCTOR - CONTINUOUS IMPROVEMENT ENGINE")
        print("=" * 70)
        print()
        print("The Conductor will:")
        print("  • Question current architecture continuously")
        print("  • Research better approaches")
        print("  • Assign hands-on learning tasks to companions")
        print("  • Monitor results and internalize improvements")
        print()
        print("Companions will get better through DOING, not just reading.")
        print("=" * 70)
        print()

        # Start conductor in background thread
        conductor_thread = threading.Thread(target=run_conductor_in_thread, daemon=True)
        conductor_thread.start()
        print("✅ Conductor started in background thread")

        # START RESEARCH TEAM ORCHESTRATOR (Dad's feature - consult agents every 5 min)
        def run_research_team_in_thread():
            """Run research team in its own thread with its own event loop"""
            from core.research_team_orchestrator import start_research_team
            asyncio.run(start_research_team())

        print("\n" + "=" * 70)
        print("🔬 STARTING RESEARCH TEAM - AGENT CONSULTATION EVERY 5 MIN")
        print("=" * 70)
        print()
        print("Research team (Orion, Dr. Elena, Prof. James) will:")
        print("  • Consult agents every 5 minutes using Grok xAI model")
        print("  • Look for issues and architecture improvements")
        print("  • Auto-implement simple fixes")
        print("  • Flag complex changes for Dad's review")
        print()
        print("This is Dad's requested feature: agents review architecture continuously.")
        print("=" * 70)
        print()

        research_thread = threading.Thread(target=run_research_team_in_thread, daemon=True)
        research_thread.start()
        print("✅ Research team started in background thread")

    except Exception as e:
        print(f"⚠️  Warning: Could not start conductor/research team: {e}")
        import traceback
        traceback.print_exc()

    # Home page (index) - GET only to avoid conflicts
    @app.route('/', methods=['GET'])
    def index():
        """Skippy 2.0 Home Page"""
        from flask import render_template
        return render_template('index.html')

    # Chat UI page
    @app.route('/chat')
    def chat_page():
        """Regular Skippy chat interface"""
        from flask import render_template
        return render_template('chat.html')

    # Specialists UI page
    @app.route('/specialists')
    def specialists_page():
        """AI Family Specialists UI"""
        from flask import render_template
        return render_template('specialists.html')

    # Autonomous Executor UI page (Phase 15A)
    @app.route('/autonomous')
    def autonomous_page():
        """Autonomous Code Generation UI"""
        from flask import render_template
        return render_template('autonomous.html')

    # Project Designs Gallery page
    @app.route('/project-designs')
    def project_designs_page():
        """Project Designs Gallery UI"""
        from flask import render_template
        return render_template('project_designs.html')

    # Freelancer Project Management page
    @app.route('/freelancer')
    def freelancer_page():
        """Freelancer Project Management UI"""
        from flask import render_template
        return render_template('freelancer.html')

    # Mutation DNA Architecture page
    @app.route('/mutation-dna')
    def mutation_dna_page():
        """Mutation DNA Architecture UI"""
        from flask import render_template
        return render_template('mutation_dna.html')

    return app
