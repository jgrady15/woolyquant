if ($env:VIRTUAL_ENV) {
    conda deactivate
    Write-Host "Deactivated the virtual environment."
}

Write-Host "Creating new virtual environment..."
conda create -n .venv python=3.11 anaconda
conda activate .venv
# Clear-Host
# pip install poetry
# poetry install
# poetry shell
