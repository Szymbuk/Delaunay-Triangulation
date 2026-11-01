"""Benchmark wyszukiwania trójkąta w gotowej triangulacji."""

from __future__ import annotations

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
class SearchBenchmarkResult:
    """Wynik pomiaru wyszukiwania trójkątów."""

    point_count: int
    query_count: int
    variant: variants
    total_seconds: float
    average_seconds: float


def _validate_points(points: PointsArray) -> None:
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("Punkty muszą mieć kształt (N, 2).")
    if points.shape[0] < 3:
        raise ValueError("Triangulacja wymaga co najmniej trzech punktów.")
    if not np.isfinite(points).all():
        raise ValueError("Współrzędne punktów muszą być skończone.")


def benchmark_triangle_search(
    points: PointsArray,
    variant: variants,
    query_count: int,
) -> SearchBenchmarkResult:
    """Zmierz wyszukiwanie trójkątów w wcześniej utworzonej triangulacji."""

    if variant not in ("JaW", "Graph"):
        raise ValueError(f'Wariant "{variant}" algorytmu wyszukiwania nie istnieje.')
    if query_count < 1:
        raise ValueError("Liczba zapytań musi być większa od zera.")

    points_array = np.asarray(points, dtype=float)
    _validate_points(points_array)

    triangulation = Triangulation(points_array.copy(), variant=variant)

    # Budowanie triangulacji nie jest częścią mierzonego wyszukiwania.
    with redirect_stdout(StringIO()):
        triangulation.triangulate()

    triangles = triangulation.get_triangles()
    if not triangles:
        raise RuntimeError("Triangulacja nie zawiera żadnych aktywnych trójkątów.")

    # Środek ciężkości aktywnego trójkąta jest zawsze punktem wewnętrznym.
    # Dzięki temu benchmark nie próbuje wyszukiwać punktów spoza triangulacji
    # ani punktów leżących na jej krawędziach.
    triangle_indices = np.random.randint(0, len(triangles), size=query_count)
    queries_array = np.asarray(
        [
            points_array[list(triangles[index])].mean(axis=0)
            for index in triangle_indices
        ]
    )

    start = perf_counter()

    for query in queries_array:
        triangulation.find_triangle(query, variant=variant)

    total_seconds = perf_counter() - start

    return SearchBenchmarkResult(
        point_count=len(points_array),
        query_count=query_count,
        variant=variant,
        total_seconds=total_seconds,
        average_seconds=total_seconds / query_count,
    )


def run_performance_analysis(
    sizes: Iterable[int] = (100, 500, 1_000, 2_000, 5_000, 10_000, 20_000, 50_000,100_000),
    *,
    queries_per_size: int = 50,
    left: float = -1_000,
    right: float = 1_000,
    variants_to_test: Iterable[variants] = ("JaW", "Graph"),
) -> list[SearchBenchmarkResult]:
    """Wykonaj benchmark wyszukiwania dla obu wariantów."""

    if queries_per_size < 1:
        raise ValueError("Liczba zapytań musi być większa od zera.")

    results: list[SearchBenchmarkResult] = []

    for size in sizes:
        if size < 3:
            raise ValueError("Rozmiary danych muszą być nie mniejsze niż 3.")

        points = generate_uniform_points(left, right, size)

        for variant in variants_to_test:
            result = benchmark_triangle_search(points, variant, queries_per_size)
            results.append(result)

            print(
                f"{result.variant:>5} | "
                f"N={result.point_count:<6} | "
                f"zapytania={result.query_count:<6} | "
                f"łącznie={result.total_seconds:.6f} s | "
                f"średnio={result.average_seconds:.9f} s"
            )

    return results


def plot_results(results: Iterable[SearchBenchmarkResult]) -> None:
    """Narysuj średni czas wyszukiwania dla obu wariantów."""

    results_by_variant: dict[variants, list[SearchBenchmarkResult]] = {
        "JaW": [],
        "Graph": [],
    }

    for result in results:
        results_by_variant[result.variant].append(result)

    plt.figure(figsize=(10, 6))

    for variant, variant_results in results_by_variant.items():
        if not variant_results:
            continue

        plt.plot(
            [result.point_count for result in variant_results],
            [result.average_seconds for result in variant_results],
            marker="o",
            label=variant,
        )

    plt.xlabel("Liczba punktów triangulacji")
    plt.ylabel("Średni czas wyszukiwania [s]")
    plt.title("Czas znalezienia trójkąta w gotowej triangulacji")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    benchmark_results = run_performance_analysis()
    plot_results(benchmark_results)