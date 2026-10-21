"""Declare the C.10 registry selectors from the complete exercise identities."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from numerics.class_exhibit import CASES
from numerics.io import read_csv, write_csv


def main() -> None:
    original = read_csv("paper/quantity_manifest.csv")
    rows = [r for r in original if r["exercise"] != "C.10"]
    fields = list(original[0])

    def add(name: str, definition: str, parameter_set: str, source: str, selector: dict,
            display: str = "decimal_6", units: str = "probability") -> None:
        rows.append(dict(zip(fields, (name, definition, "C.10", parameter_set, source,
                    "; ".join(f"{k}={v}" for k,v in selector.items()), display, units, "", "no"))))

    for row in read_csv("numerics/class_bounds.csv"):
        declaration = {key:row[key] for key in CASES[0].columns()}
        add(row["quantity"], row["definition"], "base", "numerics/class_bounds.csv",
            {**declaration,"branch":row["branch"],"quantity":row["quantity"],"column":"value"},
            row["display_format"], row["units"])
    for case in CASES:
        for row in [r for r in read_csv("numerics/class_exhibit.csv") if r["case"] == case.name]:
            for key in ("E", "O_H", "W_H", "tau", "x_star"):
                if row[key] in ("n/a", "unattainable", "always"):
                    continue
                add(f"class_{case.name}_{row['node']}_{key}", f"{key} in class exhibit {case.name} at {row['node']}.",
                    case.name, "numerics/class_exhibit.csv",
                    {**case.columns(),"r":row["r"],"node":row["node"],"branch":row["branch"],"column":key},
                    units="order units" if key == "x_star" else "probability")
            if row["node"] == "r_0":
                for key in ("m", "M", "kappa"):
                    add(f"class_{case.name}_{key}", f"General-prior {key} for class exhibit {case.name}.", case.name,
                        "numerics/class_exhibit.csv", {**case.columns(),"r":row["r"],"node":row["node"],
                        "branch":row["branch"],"column":key})
        for key in ("A1_lower", "A1_upper", "A2_lower", "A2_upper", "collapse_exclusion", "collapse_trade",
                    "ownership_sufficient", "ownership_positive_base", "ownership_exact"):
            add(f"class_{case.name}_{key}", f"{key} margin for class exhibit {case.name}; a failed comparison remains visible.",
                case.name, "numerics/class_conditions.csv", {**case.columns(),"condition":key,"column":"margin"},
                units="bound" if key.startswith("ownership") else "payoff margin")
    write_csv("paper/quantity_manifest.csv", fields, rows)
    print(f"Declared {len(rows)-len(original)} additional registry quantities; {len(rows)} total.")


if __name__ == "__main__":
    main()
