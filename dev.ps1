# EarthCARE Downloader Development Scripts
# PowerShell equivalent of Makefile for Windows users

param(
    [Parameter(Position=0)]
    [ValidateSet('help', 'install', 'install-dev', 'test', 'format', 'lint', 'clean', 'build', 'upload', 'run-gui', 'run-example', 'setup-env', 'validate-env')]
    [string]$Command = 'help'
)

function Show-Help {
    Write-Host "Available commands:" -ForegroundColor Green
    Write-Host "  install      Install dependencies"
    Write-Host "  install-dev  Install development dependencies"  
    Write-Host "  test         Run tests"
    Write-Host "  format       Format code with black"
    Write-Host "  lint         Run linting with flake8"
    Write-Host "  clean        Clean build artifacts"
    Write-Host "  build        Build package"
    Write-Host "  upload       Upload to PyPI (requires credentials)"
    Write-Host "  run-gui      Run the GUI application"
    Write-Host "  run-example  Run basic usage example"
    Write-Host "  setup-env    Show environment setup instructions"
    Write-Host "  validate-env Validate environment variables"
    Write-Host ""
    Write-Host "Usage: .\dev.ps1 <command>" -ForegroundColor Yellow
}

function Install-Dependencies {
    Write-Host "Installing dependencies..." -ForegroundColor Green
    pip install -r requirements_gui.txt
}

function Install-DevDependencies {
    Write-Host "Installing development dependencies..." -ForegroundColor Green
    pip install -r requirements_gui.txt
    pip install black flake8 pytest pytest-cov build twine
}

function Run-Tests {
    Write-Host "Running tests..." -ForegroundColor Green
    python -m pytest tests/ -v
}

function Format-Code {
    Write-Host "Formatting code with black..." -ForegroundColor Green
    python -m black .
}

function Run-Lint {
    Write-Host "Running linting with flake8..." -ForegroundColor Green
    python -m flake8 .
}

function Clean-Build {
    Write-Host "Cleaning build artifacts..." -ForegroundColor Green
    if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
    if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
    Get-ChildItem -Recurse -Directory -Name "__pycache__" | Remove-Item -Recurse -Force
    Get-ChildItem -Recurse -File -Name "*.pyc" | Remove-Item -Force
}

function Build-Package {
    Clean-Build
    Write-Host "Building package..." -ForegroundColor Green
    python -m build
}

function Upload-Package {
    Build-Package
    Write-Host "Uploading to PyPI..." -ForegroundColor Green
    python -m twine upload dist/*
}

function Run-GUI {
    Write-Host "Starting GUI application..." -ForegroundColor Green
    python earthcare_downloader_gui.py
}

function Run-Example {
    Write-Host "Running basic usage example..." -ForegroundColor Green
    python examples/basic_usage.py
}

function Setup-Environment {
    Write-Host "Environment Setup Instructions:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please set the following environment variables:" -ForegroundColor Green
    Write-Host "PowerShell:"
    Write-Host '  $env:OADS_USERNAME="your_username"' -ForegroundColor Cyan
    Write-Host '  $env:OADS_PASSWORD="your_password"' -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Command Prompt:"
    Write-Host "  set OADS_USERNAME=your_username" -ForegroundColor Cyan
    Write-Host "  set OADS_PASSWORD=your_password" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Or add them to your Windows environment variables permanently." -ForegroundColor Yellow
}

function Validate-Environment {
    Write-Host "Validating environment variables..." -ForegroundColor Green
    
    $username = [Environment]::GetEnvironmentVariable("OADS_USERNAME")
    $password = [Environment]::GetEnvironmentVariable("OADS_PASSWORD")
    
    if ($username) {
        Write-Host "✓ OADS_USERNAME set" -ForegroundColor Green
    } else {
        Write-Host "✗ OADS_USERNAME not set" -ForegroundColor Red
    }
    
    if ($password) {
        Write-Host "✓ OADS_PASSWORD set" -ForegroundColor Green
    } else {
        Write-Host "✗ OADS_PASSWORD not set" -ForegroundColor Red
    }
    
    if (-not $username -or -not $password) {
        Write-Host ""
        Write-Host "Run '.\dev.ps1 setup-env' for setup instructions." -ForegroundColor Yellow
    }
}

# Execute the specified command
switch ($Command) {
    'help' { Show-Help }
    'install' { Install-Dependencies }
    'install-dev' { Install-DevDependencies }
    'test' { Run-Tests }
    'format' { Format-Code }
    'lint' { Run-Lint }
    'clean' { Clean-Build }
    'build' { Build-Package }
    'upload' { Upload-Package }
    'run-gui' { Run-GUI }
    'run-example' { Run-Example }
    'setup-env' { Setup-Environment }
    'validate-env' { Validate-Environment }
    default { Show-Help }
}