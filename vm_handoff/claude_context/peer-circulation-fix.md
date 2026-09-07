---
name: peer-circulation-fix
description: "2026-09-05 execution of CCC_Peer_Circulation_Fixing_Spec.md on branch peer-circulation-fix; decisions taken, stage layout, gotchas"
metadata: 
  node_type: memory
  type: project
  originSessionId: b1216b8b-72db-4131-8936-6f28dcd5c5fc
  modified: 2026-09-05T22:30:53.763Z
---

On 2026-09-05 Austin asked for `~/Downloads/CCC_Peer_Circulation_Fixing_Spec.md` (Astra's spec, written after the E2E review `CCC_Assembled_Manuscript_E2E_Review.md`) to be executed end to end. Work is on branch `peer-circulation-fix` (from `codex/polish-working-paper`); internal records live in `audit/peer_polish/`.

**Decisions:**
- Voice stays first-person singular "I". The spec says restore "we", but Austin chose "I" on 2026-09-05 (HANDOFF.md rewrite section, [[working-style-feedback]]); recorded as a deviation from P21.
- The spec's companion `reference_material/` folder and `reference_oracles.py` were not delivered; only the spec and review exist in Downloads. Local PDFs hash-match the reviewed baseline exactly.
- No VM exists on this machine; "use vm" was interpreted as running heavy reruns detached/in background (or remote agent isolation if available).

**Stopped 2026-09-05 late evening at Austin's request** at commit `dfea7f9`. S0, S1-A, S1-D, S2, S3 audit, S4 main text and paper appendix are done; S1-B checks, S3 C.2 patches, S4 online appendix, S5 tables/registry were interrupted mid-work and committed as a WIP snapshot; C.6 rerun was killed; figures, S6, S7 not started.

**How to apply:** Resume from `audit/peer_polish/HANDOFF_SNAPSHOT.md` (stage table and resume order). Do not redo finished stages. Treat `numerics/exercises/c2_correspondence.py` as unverified until its quick run and tests pass. Keep singular voice. See [[numerics-build-status]] for run economics.
