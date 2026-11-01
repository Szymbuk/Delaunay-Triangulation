from contextlib import redirect_stdout
from dataclasses import dataclass
from io import StringIO
from time import perf_counter
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np

from Project.delaunay import Triangulation
from Project.utils.custom_types import PointsArray, variants
from Project.utils.generators.generate_points import generate_uniform_points


@dataclass(frozen=True)
class BenchmarkResult:
    """Measurements and output size for one triangulation run."""

    point_count: int
    triangle_count: int
    elapsed_seconds: float
    variant: variants


def _validate_points(points: PointsArray) -> None:
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("Punkty muszą mieć kształt (N, 2).")
    if points.shape[0] < 3:
        raise ValueError("Triangulacja wymaga co najmniej trzech punktów.")
    if not np.isfinite(points).all():
        raise ValueError("Współrzędne punktów muszą być skończone.")


def benchmark_triangulation(
    points: PointsArray,
    variant: variants = "JaW",
) -> BenchmarkResult:
    """Run the current triangulation implementation and measure its total time.

    ``points`` must be a floating-point-compatible NumPy array with shape
    ``(N, 2)``. The triangulation mutates its input by appending the enclosing
    triangle, so the benchmark always passes it a private copy.
    """

    if variant not in ("JaW", "Graph"):
        raise ValueError(f'Wariant "{variant}" algorytmu wyszukiwania nie istnieje.')

    points_array = np.asarray(points, dtype=float)
    _validate_points(points_array)

    triangulation = Triangulation(points_array.copy(), variant=variant)
    start = perf_counter()
    # The implementation currently logs every inserted point to stdout. Keep
    # that diagnostic out of benchmark output without changing the algorithm.
    with redirect_stdout(StringIO()):
        triangulation.triangulate()
    elapsed = perf_counter() - start

    return BenchmarkResult(
        point_count=len(points_array),
        triangle_count=len(triangulation.get_triangles()),
        elapsed_seconds=elapsed,
        variant=variant,
    )


def run_performance_analysis(
    sizes: Iterable[int] = (100, 500, 1_000, 2_000, 5_000,10_000, 20_000, 50_000),
    *,
    left: float = -1_000,
    right: float = 1_000,
    variants_to_test: Iterable[variants] = ("JaW", "Graph"),
) -> list[BenchmarkResult]:
    """Benchmark each configured variant for each generated input size."""

    results: list[BenchmarkResult] = []
    for size in sizes:
        if size < 3:
            raise ValueError("Rozmiary danych benchmarku muszą być nie mniejsze niż 3.")
        points = generate_uniform_points(left, right, size)
        for variant in variants_to_test:
            result = benchmark_triangulation(points, variant)
            results.append(result)
            print(
                f"{result.variant:>5} | N={result.point_count:<6} | "
                f"trójkąty={result.triangle_count:<6} | "
                f"czas={result.elapsed_seconds:.4f} s"
            )
    return results


def plot_results(results: Iterable[BenchmarkResult]) -> None:
    """Plot total triangulation time grouped by point-location variant."""

    results_by_variant: dict[variants, list[BenchmarkResult]] = {"JaW": [], "Graph": []}
    for result in results:
        results_by_variant[result.variant].append(result)

    plt.figure(figsize=(10, 6))
    for variant, variant_results in results_by_variant.items():
        if variant_results:
            plt.plot(
                [result.point_count for result in variant_results],
                [result.elapsed_seconds for result in variant_results],
                marker="o",
                label=variant,
            )
    plt.xlabel("Liczba punktów")
    plt.ylabel("Czas [s]")
    plt.title("Czas triangulacji Delaunaya")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_results(run_performance_analysis())
