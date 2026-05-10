# COSC3000 - Computer Graphics Project
**Student:** Dzaky Zhafran Razzansyah  
**Course:** COSC3000 Semester 1, 2026  
**University of Queensland**

---

## Overview

This project implements 3D computer graphics techniques applied to a low-polygon cow mesh in OBJ format. It demonstrates geometric transformations using 4×4 transformation matrices and direction-determined face colouring using the dot product.

---

## Features

- OBJ file loader
- Geometric transformations using explicit 4×4 matrices:
  - Translation
  - Rotation (X, Y, Z axes)
  - Combined translation and rotation
  - Scaling
  - Shear (shape-changing transformation)
- Dot-product face colouring based on light source direction
- Before/after visualisation for each transformation

---

## Requirements

- Python 3.x
- NumPy
- Matplotlib

Install dependencies with:

```bash
pip install numpy matplotlib
```

---

## Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows (Git Bash)
source venv/bin/activate       # Mac/Linux

# Install dependencies
pip install numpy matplotlib
```

---

## Usage

Place your OBJ file in the `3d_models/` folder, then update the filename at the top of `graphics_starter.py`:

```python
OBJ_FILE = "3d_models/cow.obj"
```

Run the script:

```bash
python graphics_starter.py
```

This will open one window per transformation showing the before/after comparison, plus a separate window for the dot-product colouring. All outputs are also saved as PNG files in the project root.

---

## Project Structure

```
s4894855_ComputerGraphics/
├── 3d_models/
│   └── cow.obj
├── venv/
├── graphics_starter.py
├── .gitignore
└── README.md
```

---

## Output Files

| File | Description |
|------|-------------|
| `transform_1_Translation.png` | Before/after translation |
| `transform_2_Rotation_Y_45deg.png` | Before/after rotation |
| `transform_3_Translation_and_Rotation.png` | Before/after combined transform |
| `transform_4_Scaling_x2.png` | Before/after scaling |
| `transform_5_Shape_Change.png` | Before/after shear |
| `dot_product_colouring.png` | Direction-determined face colouring |
