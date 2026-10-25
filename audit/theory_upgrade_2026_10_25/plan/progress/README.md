# Stage reports

The coordinator reads PLAN.md, DECISIONS.md and every report here before continuing. The merged PLAN.md governs the stage order; the lens files retain earlier alternatives for reference.

Each stage writes `S<n>.md` with the date, starting revision, work completed, files changed, commands run with real inputs, observed outputs, pages read, language-scan judgments, number reconciliation where relevant, unresolved items and the next eligible stage. State whether the stage gate is complete or blocked. Report completion only after the required outputs have been inspected. S5 packages may use `S5_<package>.md`, followed by a consolidated S5 report.

`S0_setup.md` records infrastructure and source comparison. `S0_smoke.md` records the initial builds and numbers pipeline. These do not by themselves complete S0's label baseline. A later work period resumes from the latest completed stage report and does not repeat completed work without a reason.

No automatic schedule is used. Do not begin a second writer on a branch with unfinished work. If `LOCK` is present, inspect its recorded UTC time and stage; a lock less than three hours old means stop. Do not remove a stale lock without checking the recorded unfinished work. Remove a lock owned by this work period when it ends.

Use the programs through their documented interfaces and report their output. Do not author or extend tests, fixtures or testing frameworks, and do not run a test suite. Recommendations in DECISIONS.md are not answers. Stop at S1 until Austin answers all decisions; stop before final delivery to the manuscript service.

Every completed stage ends with its report, a plain content commit, and a push of `theory-upgrade` only. No force-push, merge into `main`, pull request or delivery push is authorized by these records.
