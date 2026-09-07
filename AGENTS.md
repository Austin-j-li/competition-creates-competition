# Project guidance

Read `CLAUDE.md` before editing. Follow `handout/README.md` for the supervisor handout,
`learn/MISSION.md` for the teaching course, and `replication/README.md` for research builds.
`VM_START_HERE.md` and the VM checkpoints describe a completed revision, not pending work.

An agent may spawn at most six direct subagents in one batch. Subagents may not spawn subagents.

Show economic models and LaTeX as rendered equations. Use native math rendering in desktop
chat. If an image is needed, render a local PNG with an available TeX or plotting tool.
Do not assume the VM-specific `eq` terminal command is installed on another machine.
