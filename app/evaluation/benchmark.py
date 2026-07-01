import csv
from pathlib import Path


class Benchmark:

    def __init__(self):

        self.results = []

    def add_result(
        self,
        query,
        metrics,
        latency,
    ):

        row = {

            "Query": query,

            "Hit@K": metrics[
                "Hit@K"
            ],

            "Precision@K": metrics[
                "Precision@K"
            ],

            "Recall@K": metrics[
                "Recall@K"
            ],

            "MRR": metrics[
                "MRR"
            ],

            "Latency(sec)": latency,

        }

        self.results.append(
            row
        )

    def save_csv(
        self,
        output_path="storage/benchmark.csv",
    ):

        Path(
            output_path
        ).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_path,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=self.results[
                    0
                ].keys(),
            )

            writer.writeheader()

            writer.writerows(
                self.results
            )

        print(
            f"\nBenchmark saved to {output_path}"
        )