# Peer-circulation revision: historical VM handoff

For current cross-machine updates, follow `README.md`. The current paper, handout, course,
and shared project instructions are on `main`. The interrupted-work instructions below
are retained as history; the revision is complete.

## Completed on 2026-09-06

The peer-circulation revision is complete in the audited working-paper scope. Read `audit/peer_polish/completion_report.md` for final results, limits and provenance. The validated scientific source revision is `6aac3caacb7a0fc819795a423d4fb7363eb58371`; the final audit commit records delivery.

The peer PDFs are `peer_release/main.pdf` and `peer_release/online_appendix.pdf`. The source package is `source_and_replication.tar.gz`; `replication/delivery_checksums.json` records its external checksum. Fresh reproduction matched all 29 CSV outputs and both final manuscript texts; all 47 tests, 186 certificate checks and 129 page inspections passed. No interrupted numerical job remains to resume.

The transfer instructions below are preserved as historical context.

This is the transferred work in progress, not a validated peer release. The transfer task did not resume the research or rebuild its outputs.

## Read first

1. `audit/peer_polish/HANDOFF_SNAPSHOT.md`, the current stopped-stage record.
2. `vm_handoff/inputs/CCC_Peer_Circulation_Fixing_Spec.md`, the execution specification.
3. `vm_handoff/inputs/CCC_Assembled_Manuscript_E2E_Review.md`, the supporting review.
4. `CLAUDE.md`, then `audit/peer_polish/repository_map.md` and the appendix sections needed for the active stage.
5. `vm_handoff/claude_context/peer-circulation-fix.md` and `working-style-feedback.md` for the saved decisions.

The top-level `HANDOFF.md` is the original build brief. It predates the completed build and the current revision; do not restart that original task.

## Exact starting state

- Source commit: `dfea7f9a01c46a92f1d2c678bfe775217ccaf51d`, branch `peer-circulation-fix`. The handoff's shorter `b559338` reference denotes the preceding WIP commit; `dfea7f9` adds the handoff itself.
- Destination: `/home/uctpiaj/work/competition-creates-competition` on `econ-phd-04`, SSH alias `condenser-vm`.
- The older `/home/uctpiaj/work/ccc` directory is a separate earlier copy. Work in this destination.
- Full Git history and a standalone `vm_handoff/repository.bundle` are included. No commits or pushes were made during transfer.
- Local uncommitted state is preserved: deleted `docs/main_filled.pdf`, untracked `docs/manuscript.pdf`, and untracked `learn/`. Treat these and the handout work as foreign to this revision. Keep them intact and stage only revision files. See `vm_handoff/source_status.txt` and `source_diff.patch`.
- Generated figures, manuscript PDFs, ignored `paper/drafts/`, and interrupted-run logs are included. Existing PDFs still match the reviewed baseline; they do not represent the unfinished edits.
- Machine-local `.venv`, `.claude/settings.local.json`, caches, `.DS_Store`, and `paper/build/` were omitted. A fresh Linux `.venv` is prepared separately. Source Python package pins are in `vm_handoff/requirements-source.txt`.

## Decisions and missing material

Keep first-person singular “I”. Claude recorded the author's decision as overriding the spec's “we” instruction. Record the deviation from P21 in the eventual completion report.

The promised companion `reference_material/`, `reference_oracles.py`, and its `oracle_run/` outputs were not supplied and were not found during the targeted local search. The provided verification seed, its audit copy, source bibliography, and hash-matched reviewed PDFs are included. Preserve this limitation rather than claiming that the missing independent package was run.

Historic notes saying that no VM exists are superseded by this transfer. Absolute Mac paths in the old notes identify their original sources. The two Downloads documents are now under `vm_handoff/inputs/`.

The writing guidance requested by the author is included at `vm_handoff/unslop.md`. Earlier references to optional local delegation tools are historical context, not required runtime dependencies. An agent may spawn at most six direct subagents in a batch; subagents may not spawn further subagents. When showing equations to the user, use `eq` as requested in the original session; its cmux display setup is machine-specific and is not part of this package.

## Continue in the recorded order

Start with `git status` and the handoff's resume order. Check `vm_handoff/VM_ENVIRONMENT.md` for the environment setup result before running commands. Activate the project environment so the renderer can find its local pandoc executable:

```bash
cd /home/uctpiaj/work/competition-creates-competition
source .venv/bin/activate
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
```

Finish the interrupted C.2 implementation and its quick tests before a full run. For a diagnostic run, the current C.2 CLI supports `--out=...`; use a distinct audit directory to preserve full outputs. Set explicit worker counts for C.2/C.6, initially eight each, rather than their CPU-count defaults on this 64-CPU VM. Check current load before increasing concurrency.

S1-B independent checks, S3 C.2, S4 online appendix alignment, S5 registry/tables/figures, and S6/S7 remain unfinished as detailed in the handoff. Existing CSVs, filled sources, and WIP code must not be treated as newly verified results. No heavy reruns were started by the transfer session.

The eventual completion criterion is the specification's retained-content checks, final verification gate, full PDF inspection, peer package, replication archive, and honest completion report. A successful transfer or dependency smoke check does not meet those research gates. No emailing, public publishing, or sending the paper is authorized.
