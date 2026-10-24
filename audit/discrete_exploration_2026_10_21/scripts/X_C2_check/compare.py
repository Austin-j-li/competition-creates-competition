# Read saved two-round output records and print fields for comparison.
# Prints values only.
import json

PATH = "audit/discrete_exploration_2026_10_21/scripts/C2_two_rounds/results.jsonl"
rows = []
with open(PATH, "r", encoding="utf-8") as handle:
    for line in handle:
        line = line.strip()
        if line:
            rows.append(json.loads(line))
print("records =", len(rows))
for idx, row in enumerate(rows):
    keys = sorted(row.keys())
    print("--- record", idx, "keys:", ",".join(keys[:12]))
    if "name" in row:
        print("  name =", row.get("name"), "life =", row.get("life"),
              "noise =", row.get("noise"), "r =", row.get("r"),
              "k =", row.get("k"), "beta =", row.get("beta"), "a =", row.get("a"))
        print("  entry =", row.get("entry"))
        print("  high_ownership =", row.get("high_ownership"))
        print("  high_expected_units =", row.get("high_expected_units"))
        print("  high_total_cost =", row.get("high_total_cost"))
        print("  high_total_net_profit =", row.get("high_total_net_profit"))
        print("  first_action_values =", row.get("first_action_values"))
        margins = row.get("terminal_choice_margins", [])
        print("  margins count =", len(margins))
        for m in margins:
            print("    margin", m)
        print("  private_best_orders =", row.get("private_best_orders"))
        # Prices for laplace benchmark short full at float a.
        if row.get("name") == "laplace_benchmark":
            print("  price1 =", row.get("price1"))
            term = row.get("terminal", {})
            for key in sorted(term.keys()):
                print("    terminal", key, term[key])
    if "kind" in row:
        print("  kind =", row.get("kind"), "a =", row.get("a"), "r =", row.get("r"))
        for field in ["first_good", "posterior_two_good", "B_one_good", "B_two_good",
                      "no_trade_cost_floor", "second_bad_gross", "second_good_gross",
                      "first_gross", "full_gross_lower_bound",
                      "endogenous_posterior_bound", "upper_posterior_supports_entry"]:
            print("   ", field, "=", row.get(field))
    if "rational_interval_margins" in row:
        print("  rational_interval_margins =", row["rational_interval_margins"])
    if "original_cost_interval_margins" in row:
        print("  original_cost_interval_margins =", row["original_cost_interval_margins"])
    if "benchmark_rational_bounds" in row:
        print("  benchmark_rational_bounds =", row["benchmark_rational_bounds"])
    if "equal_horizons" in row:
        print("  equal_horizons =", row["equal_horizons"])
print("End of comparison print.")
