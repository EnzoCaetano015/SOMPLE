# SOMPLE model v1.1.0 evaluation

Metrics use 2-fold stratified out-of-fold predictions because the smallest class has only two examples. The final artifact is fitted with all 180 rows.

## Metrics

```json
{
  "classifier": {
    "accuracy": 0.7667,
    "precision_macro": 0.5057,
    "recall_macro": 0.5223,
    "f1_macro": 0.5116,
    "per_class": {
      "low": {
        "precision": 0.5,
        "recall": 0.5,
        "f1": 0.5,
        "support": 2
      },
      "medium": {
        "precision": 0.1538,
        "recall": 0.1667,
        "f1": 0.16,
        "support": 12
      },
      "high": {
        "precision": 0.425,
        "recall": 0.5484,
        "f1": 0.4789,
        "support": 31
      },
      "critical": {
        "precision": 0.944,
        "recall": 0.8741,
        "f1": 0.9077,
        "support": 135
      }
    },
    "confusion_matrix": [
      [
        1,
        1,
        0,
        0
      ],
      [
        1,
        2,
        9,
        0
      ],
      [
        0,
        7,
        17,
        7
      ],
      [
        0,
        3,
        14,
        118
      ]
    ],
    "confusion_matrix_labels": [
      "low",
      "medium",
      "high",
      "critical"
    ]
  },
  "regressor": {
    "mae": 8.8325,
    "rmse": 11.9401,
    "r2": 0.5945
  },
  "evaluation": {
    "method": "2-fold stratified out-of-fold evaluation",
    "fold_sizes": [
      {
        "train": 90,
        "test": 90
      },
      {
        "train": 90,
        "test": 90
      }
    ],
    "final_fit_size": 180,
    "random_state": 42
  }
}
```

## Confusion matrix

| actual \ predicted | low | medium | high | critical |
| --- | --- | --- | --- | --- |
| low | 1 | 1 | 0 | 0 |
| medium | 1 | 2 | 9 | 0 |
| high | 0 | 7 | 17 | 7 |
| critical | 0 | 3 | 14 | 118 |

The simulated academic dataset is small; these metrics do not represent production performance.
