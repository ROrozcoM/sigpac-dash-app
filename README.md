# SIGPAC-DASH-APP 

Interactive web application for downloading, visualizing, and analyzing parcels from Spain's Agricultural Parcel Geographic Information System (SIGPAC).

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Dash](https://img.shields.io/badge/dash-latest-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

- **Download by SIGPAC Codes**: Enter individual parcel codes in `PR:MU:PO:PA:RE` format
- **Download from ATOM**: Bulk download of official FEGA data filtering by:
  - Province and municipality
  - Maximum area
  - Minimum slope
  - Land use (olive groves, vineyards, arable land, etc.)
- **Map Visualization**: Interactive satellite view with downloaded parcels
- **Statistics**: Number of parcels, total area, and average
- **Export**: Download in GeoPackage (.gpkg) and Shapefile (.shp) formats

## Installation

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) - Ultra-fast Python package manager

### 1. Install uv

If you don't have `uv` installed, you can install it with:

**On Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**On Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or using pip:
```bash
pip install uv
```

### 2. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/sigpac-dash-app.git
cd sigpac-dash-app
```

### 3. Create virtual environment and install dependencies

```bash
uv sync
```

This command:
- Automatically creates a virtual environment in `.venv`
- Installs all dependencies specified in `pyproject.toml`
- Sets up the project ready to use

### 5. Run your code

**From the terminal:**
```bash
uv run python main.py
```
This will start the Dash development server.
By default, the app will be available at:
http://127.0.0.1:8050

**From your code editor (VSCode, PyCharm, etc.):**
1. Open the main.py file.
2. Make sure your Python interpreter is set to the project virtual environment (.venv).
3. Click the ▶️ Run / Play button to start the app.

The development server will start automatically, and you can open the app in your browser.

## Contributing

Contributions are welcome. Please:

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Data Sources

- Data provided by [FEGA](https://www.fega.gob.es/) (Spanish Agricultural Guarantee Fund)
- SIGPAC System from the Ministry of Agriculture, Fisheries and Food of Spain

---
