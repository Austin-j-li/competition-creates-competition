"""Mathematical cutoff endpoints get tags; numerical failures stay visible."""
import csv
from pathlib import Path
from tempfile import TemporaryDirectory

from numerics.io import write_csv


def test_cutoff_tags_at_csv_boundary():
    columns = ["x_star", "x_star_Yplus", "x_star_Yminus", "error"]
    values = [float("inf"), float("-inf"), float("nan"), 1.25]
    with TemporaryDirectory() as directory:
        path = Path(directory) / "cutoffs.csv"
        write_csv(path, columns, [dict.fromkeys(columns, value) for value in values])
        with path.open(newline="") as stream:
            result = list(csv.DictReader(stream))
    for row, tag, error in zip(result, ["unattainable", "always", "n/a", "1.25"],
                               ["inf", "-inf", "nan", "1.25"]):
        assert all(row[column] == tag for column in columns[:-1])
        assert row["error"] == error
