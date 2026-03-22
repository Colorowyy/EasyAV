#!/bin/bash
# Setup script for EasyAV antivirus software
# This script creates a virtual environment and installs dependencies

set -e

echo "================================"
echo "EasyAV - Setup Script"
echo "================================"
echo ""
echo "This script will check for Python and install required dependencies."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed on your system."
    echo ""
    echo "Would you like to install Python 3.11 now? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Installing Python 3.11..."
        echo "Note: You may need to enter your password for sudo access."
        echo ""

        # Detect OS and install Python 3.11
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            if command -v apt &> /dev/null; then
                echo "Adding deadsnakes PPA for Python 3.11..."
                sudo apt update
                sudo apt install -y software-properties-common
                sudo add-apt-repository -y ppa:deadsnakes/ppa
                sudo apt update
                sudo apt install -y python3.11 python3.11-pip python3.11-venv
                # Set python3 to point to python3.11
                sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
            elif command -v dnf &> /dev/null; then
                sudo dnf install -y python3.11 python3-pip
            elif command -v pacman &> /dev/null; then
                sudo pacman -S python python-pip
            else
                echo "❌ Unsupported Linux distribution. Please install Python 3.11 manually."
                echo "Visit: https://www.python.org/downloads/"
                exit 1
            fi
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if command -v brew &> /dev/null; then
                brew install python@3.11
            else
                echo "❌ Homebrew not found. Installing Homebrew first..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                echo "Please restart your terminal and run this script again."
                exit 1
            fi
        else
            echo "❌ Unsupported operating system. Please install Python 3.11 manually."
            echo "Visit: https://www.python.org/downloads/"
            exit 1
        fi

        echo ""
        echo "✅ Python 3.11 installation complete!"
        echo "Please restart your terminal and run this setup script again."
        echo ""
        echo "After restart, you can continue with: ./setup.sh"
        exit 0
    else
        echo "❌ Python 3.11 is required to run EasyAV."
        echo "Please install Python 3.11 or higher from: https://www.python.org/downloads/"
        exit 1
    fi
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Check Python version
PYTHON_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    echo "❌ Python 3.7 or higher is required. Found Python $PYTHON_VERSION"
    echo "Please upgrade Python and try again."
    exit 1
fi

echo "✅ Python version check passed!"
echo ""

# Install requirements
if [ -f requirements.txt ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
else
    echo "Warning: requirements.txt not found"
fi

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "To run the application, execute:"
echo "  python3 main.py"
echo ""
echo "  python3 main.py"
echo ""
