# Plotly Scatter Plot Example

A Python script that creates a scatter plot with shaded regions using Plotly.

## Features

- Scatter plot with data points (most on diagonal, some off diagonal)
- Red shading below the line y = 0.8x
- Green shading above the line y = 1.2x
- Reference lines showing the boundary conditions

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script:

```bash
python plot_data.py
```

The plot will open in your default web browser.

## Data

The script generates:
- 50 points mostly on the diagonal (y ≈ x) with small random noise
- 15 points off the diagonal (some above, some below)
