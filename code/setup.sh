#!/bin/bash
# Setup script for AI Coding Workshop
# Creates virtual environments and installs dependencies for all projects

set -e  # Exit on error

echo "🚀 AI Coding Workshop - Setup Script"
echo "======================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Function to setup a project
setup_project() {
    local project_dir=$1
    local project_name=$2
    
    echo "📦 Setting up $project_name..."
    cd "$SCRIPT_DIR/$project_dir"
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "  Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    echo "  Upgrading pip..."
    pip install --upgrade pip > /dev/null
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        echo "  Installing dependencies..."
        pip install -r requirements.txt > /dev/null
        echo "  ✅ $project_name setup complete!"
    else
        echo "  ⚠️  No requirements.txt found"
    fi
    
    # Deactivate virtual environment
    deactivate
    
    echo ""
}

# Setup all projects
setup_project "01-legacy-app" "Lab 1: Legacy App"
setup_project "02-scaffold" "Lab 2: Scaffold"
setup_project "03-business-logic" "Lab 3: Business Logic"
setup_project "04-complete" "Lab 4: Complete Solution"

echo "✨ All projects setup complete!"
echo ""
echo "Usage:"
echo "  ./run-lab1.sh  - Run legacy Flask app"
echo "  ./run-lab2.sh  - Run scaffold FastAPI app"
echo "  ./run-lab3.sh  - Run business logic FastAPI app"
echo "  ./run-lab4.sh  - Run complete solution FastAPI app"
echo ""
