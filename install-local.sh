#!/bin/bash
# Install hermes-notifier locally for development/testing

echo "🚀 Installing hermes-notifier locally..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install in editable mode
echo "📥 Installing hermes-notifier in editable mode..."
pip install -e .

# Install dev dependencies
echo "🛠️ Installing dev dependencies..."
pip install -e ".[dev]"

echo ""
echo "✅ Installation complete!"
echo ""
echo "To use the package:"
echo "  source venv/bin/activate"
echo "  python examples/simple_send.py"
echo ""
echo "To deactivate:"
echo "  deactivate"

