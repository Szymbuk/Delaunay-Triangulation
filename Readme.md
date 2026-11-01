# Delaunay Triangulation

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)
![Testing](https://img.shields.io/badge/pytest-passing-success.svg)

A Python-based computational geometry project implementing the Delaunay Triangulation algorithm. The project features interactive Jupyter notebooks for step-by-step visualization, custom point generators, and efficient point-location structures to ensure mesh validity.

## 📸 Preview

![Delaunay Visualization](bitalg/visualizer/plot.gif)

*Visualization of the Delaunay Triangulation process.*

## 🚀 Features

* **Core Algorithm:** Efficient implementation of Delaunay Triangulation ensuring the circumcircle property and edge legality (`legality.py`, `orient.py`).
* **Triangle Search Strategies:** Advanced point-location algorithms including **Jump and Walk** (`jump_and_walk.py`) and **Directed Graph DFS** (`directed_graph_dfs.py`).
* **Data Generators & I/O:** Supports generating diverse datasets (random distributions, circular points, interactive mouse input) as well as importing/exporting data via CSV (`csvIO.py`).
* **Interactive Visualization:** Includes Jupyter notebooks (`main.ipynb`, `search_demo.ipynb`) for visual, step-by-step algorithmic demonstrations.
* **Extensive Testing:** Comprehensive unit, integration, and visual test suites built with `pytest` covering edge turning, triangle legality, orientation, and search accuracy.
* **Benchmarking:** Dedicated performance evaluation scripts (`traingulation_benchmark.py`, `triangle_search_test.py`) to measure execution time and algorithmic complexity.

## 💻 Tech Stack

* **Language:** Python 3.8+
* **Interactive Environment:** Jupyter Notebook
* **Visualization:** `bitalg` (Custom visualization package), `matplotlib`
* **Testing:** `pytest`

## 📂 Project Structure

* `Projekt/` – Core implementation of the Delaunay triangulation, point generators, triangle operations, search algorithms, and demonstration notebooks.
* `bitalg/` – Geometric visualization toolset used to render points, polygons, circles, and animations.
* `tests/` – Unit, integration, and visual test suites.
* `benchmarks/` – Scripts for benchmarking triangulation and search performance.

## 🛠 Getting Started

### Prerequisites

Ensure you have Python 3.8 or newer installed on your machine.

### Installation

1. Clone the repository:
   git clone https://github.com/Szymbuk/Delaunay-Triangulation.git

2. Navigate to the project directory:
   cd Delaunay-Triangulation

3. Install the required dependencies:
   pip install -r requirements.txt

## 📖 Usage

### Interactive Notebooks

To see the triangulation algorithm in action and interact with the visualizations, launch Jupyter Notebook:

   jupyter notebook Projekt/main.ipynb

To explore and compare the triangle search algorithms (Jump and Walk vs. Directed Graph DFS):

   jupyter notebook Projekt/search_demo.ipynb

### Running Tests

To execute the unit and integration test suites using `pytest`, run the following command in the root directory:

   pytest

### Running Benchmarks

To evaluate the performance of the implemented algorithms, run the benchmark scripts:

   python -m benchmarks.traingulation_benchmark

## 👏 Acknowledgments

* **`bitalg` Visualizer:** The geometric visualization package located in the `bitalg/` directory was created and provided by the **BIT Scientific Circle (Koło Naukowe BIT)** at AGH University of Krakow for the Computational Geometry course (*Algorytmy Geometryczne*).

## 📝 License

This project is open-source and available under the MIT License.