"""Print the page of each section heading in build/main.pdf (first page whose text starts a line with the heading)."""
import subprocess, sys, re
pdf = sys.argv[1]
n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
heads = ["1 Introduction", "2 The model", "3 Competition and information", "4 Equilibrium results",
         "5 Competition creates research", "6 Robustness", "7 Welfare and sale terms", "8 Empirical implications",
         "9 Conclusion", "References", "A Proofs", "A.2 Beliefs", "A.3 Competition", "A.4 Coexistence", "A.5 Research",
         "A.6 Robustness", "A.7 Welfare", "A.8 Empirical", "A.9 Parameter"]
found = {}
for p in range(1, n + 1):
    t = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), "-layout", pdf, "-"], capture_output=True, text=True).stdout
    for h in heads:
        if h not in found and re.search(r"^\s*" + r"\s+".join(map(re.escape, h.split())), t, re.M):
            found[h] = p
for h in heads:
    print(f"{found.get(h, '?'):>4}  {h}")
print(f"{n:>4}  total pages")
if "References" in found and "1 Introduction" in found:
    print("main text pages", found["1 Introduction"], "to", found["References"] - 1, "=", found["References"] - found["1 Introduction"])
if "A Proofs" in found:
    print("appendix pages", found["A Proofs"], "to", n, "=", n - found["A Proofs"] + 1)
