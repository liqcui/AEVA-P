#!/bin/bash
# AEVA Docker Entrypoint Script

set -e

echo "🚀 AEVA v2.0 Docker Container"
echo "=============================="

# Function to check if production libraries are available
check_production_libs() {
    echo "Checking production libraries..."

    if python -c "import art" 2>/dev/null; then
        echo "✅ ART (Adversarial Robustness Toolbox) available"
    else
        echo "⚠️  ART not available, using fallback"
    fi

    if python -c "import great_expectations" 2>/dev/null; then
        echo "✅ Great Expectations available"
    else
        echo "⚠️  Great Expectations not available, using fallback"
    fi

    if python -c "import statsmodels" 2>/dev/null; then
        echo "✅ statsmodels available"
    else
        echo "⚠️  statsmodels not available, using fallback"
    fi

    if python -c "import streamlit" 2>/dev/null; then
        echo "✅ Streamlit available"
    else
        echo "⚠️  Streamlit not available"
    fi

    echo ""
}

# Function to run quick tests
run_quick_tests() {
    echo "Running quick tests..."
    python examples/run_all_quick_tests.py
}

# Function to run full tests
run_full_tests() {
    echo "Running full test suite..."
    python -m pytest tests/ -v
}

# Function to start dashboard
start_dashboard() {
    echo "Starting AEVA dashboard..."
    if python -c "import streamlit" 2>/dev/null; then
        streamlit run aeva/dashboard/app.py --server.port=8501 --server.address=0.0.0.0
    else
        echo "❌ Streamlit not installed. Install with: pip install streamlit"
        exit 1
    fi
}

# Function to show help
show_help() {
    cat << EOF

AEVA v2.0 Docker Container Commands
====================================

Available commands:

  quick-tests          Run quick functionality tests
  full-tests          Run full pytest suite
  dashboard           Start Streamlit dashboard (port 8501)
  production-demo     Run production integrations demo
  check-libs          Check production library availability
  shell               Start interactive bash shell
  python              Start Python REPL
  help                Show this help message

Examples:

  docker run aeva quick-tests
  docker run -p 8501:8501 aeva dashboard
  docker run -it aeva shell

With docker-compose:

  docker-compose run aeva quick-tests
  docker-compose up aeva-dashboard

EOF
}

# Main command dispatcher
case "$1" in
    quick-tests)
        check_production_libs
        run_quick_tests
        ;;
    full-tests)
        check_production_libs
        run_full_tests
        ;;
    dashboard)
        check_production_libs
        start_dashboard
        ;;
    production-demo)
        check_production_libs
        python examples/production_integrations_example.py
        ;;
    check-libs)
        check_production_libs
        ;;
    shell)
        exec /bin/bash
        ;;
    python)
        exec python
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        if [ -z "$1" ]; then
            show_help
        else
            # Execute custom command
            exec "$@"
        fi
        ;;
esac
