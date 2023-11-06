if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
    echo "Deactivated the virtual environment."
fi
if [ -d "$.venv" ]; then
    rm -rf "$.venv"
    echo "Removed current virtual environment directory."
fi

echo "Creating new virtual environment..."
rm -rf .venv
py -3.11 -m venv .venv
source ../.venv/bin/activate


