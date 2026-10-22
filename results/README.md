# Results Directory Organization

This directory contains verified experimental outputs, standardized tables, publication figures, and statistical test outputs:

- `results/canonical/`: Mirror of authoritative outputs from `experiments/results_canonical/`:
  - `canonical_test_predictions.csv`: Per-instance test predictions ($N=163$).
  - `canonical_dev_predictions.csv`: Development split predictions ($N=103$).
  - `canonical_benchmark_table.csv`: 4-condition benchmark and ablation table.
  - `canonical_dev_tuning.csv`: Complete grid search evaluation across candidate thresholds.
  - `canonical_random_control_100seeds.csv`: Multi-seed simulation evaluation of the matched-coverage random baseline.
  - `test_metrics.json`: Hierarchical JSON serialization of all canonical sensitivity metrics.
- `results/statistical_tests/`: Detailed pairwise statistical test records (McNemar exact tests, permutation tests, FDR adjustments).
- `results/tables/`: LaTeX and CSV tables prepared for the manuscript.
- `results/figures/`: Publication-quality figures (vector PDF and PNG) generated deterministically from canonical data.
