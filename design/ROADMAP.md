# Development roadmap — close the gap with `ARCHITECTURE.md`

Actionable backlog derived from [`ARCHITECTURE.md`](ARCHITECTURE.md). Use checkboxes locally; prioritize within each phase by risk and dependencies.

**Legend:** “Arch n” = section **n** in `ARCHITECTURE.md`.

---

## Implementation snapshot (2026-04)

Ground truth for planning; update when behavior changes.

| Area | Status |
|------|--------|
| **Git / index** | Run `git restore --staged .` if the index had mass accidental deletes; verify with `git status`. |
| **`ReloadCommands` / `SetMuted`** | **Implemented** in `jarvis-app` `main.rs`: reload updates `COMMANDS_LIST` + `intent::reload`; mute uses `MIC_MUTED` and `app.rs` gates wake/STT. |
| **Frontend IPC** | `reloadCommands()`, `setMuted()`, `micMuted` store; Settings → General → running assistant actions. |
| **Mute / reload events** | **`MicMuted`**, **`CommandsReloaded`** on `IpcEvent` (`events.rs`). |

**Suggested next slice:** **P1.4** (short `design/ipc.md` or expand comments), then **P2** (router).

---

## Phase 0 — Baseline & hygiene

Foundation before large features.

- [ ] **P0.1** Align repo state: ensure tracked files match `HEAD` (fix accidental full-index deletes / untracked duplicates) so CI and collaborators see a clean tree.
- [ ] **P0.2** Refresh root **README** vs `ARCHITECTURE.md`: stack, build, planned LLM/router/voice story, and i18n reality (README still says “only Russian”; app has en/ru/ua assets in places).
- [ ] **P0.3** Document minimum versions: Rust, Node, platform notes (Windows AHK, macOS tray limits) in README or a new `BUILD.md`.

---

## Phase 1 — IPC & assistant control (Arch 4, Arch 12)

Closes stubbed behavior called out in architecture.

- [x] **P1.1** Implement **`IpcAction::ReloadCommands`**: re-parse `resources/commands/`, refresh `COMMANDS_LIST`, re-init or hot-reload intent training data as needed (`jarvis-app` + `commands`/`intent` modules).
- [x] **P1.2** Implement **`IpcAction::SetMuted { muted }`**: gate mic processing / wake / STT when muted; emit clear `IpcEvent` state for GUI.
- [x] **P1.3** GUI: add `setMuted` in `ipc.ts`, optional store for mic muted state, and settings (or header) controls for **mute** and **reload**; call existing `reloadCommands()` where appropriate.
- [ ] **P1.4** Audit **WebSocket** message schema vs frontend `ipc.ts` — document `IpcEvent` / `IpcAction` variants in one place (comment in `events.rs` + `ipc.ts`, or small `design/ipc.md`).

---

## Phase 2 — Intelligence router (Arch 6–7)

Explicit **fast path vs LLM path** in `jarvis-app` after STT.

- [ ] **P2.1** Introduce a **`Router`** (module or type) after transcript: inputs = text + intent confidence; outputs = `FastPathExecute { command_id, … }` | `NeedsLlm { reason }` | `Clarify`.
- [ ] **P2.2** Define **confidence thresholds** and “abstain” rules in **settings** or config (per-language optional).
- [ ] **P2.3** Ensure **fast path** always ends with existing execution + **`voices::play(Reaction)`** + IPC — no placeholder calls.
- [ ] **P2.4** **`jarvis-cli`**: add or extend subcommands to simulate **router** decisions (dump why LLM would be chosen).

---

## Phase 3 — LLM facade & backends (Arch 7, principles 3–4)

Single Rust API; multiple backends.

- [ ] **P3.1** Define trait/facade in **`jarvis-core`** (feature-gated): e.g. `LlmBackend::chat(ChatRequest) -> ChatResponse` with **messages + optional tools** (serde types aligned with OpenAI chat schema).
- [ ] **P3.2** Implement **`OpenAiCompatibleHttpBackend`**: `base_url`, `api_key`, `model`, `reqwest`; supports **streaming** optional for later.
- [ ] **P3.3** Validate against **Ollama** and **`llama-server`** (OpenAI-compatible mode) on loopback — document example URLs in README.
- [ ] **P3.4** **Embedded or child-process `llama.cpp`**: pick one initial strategy (recommended: **managed `llama-server` child** for fewer FFI risks) behind the same trait; document path to in-process later.
- [ ] **P3.5** **Settings & DB**: persist `llm_enabled`, `llm_base_url`, `llm_api_key`, `llm_model`, `llm_backend_kind` (http_local | http_remote | bundled_server); extend `db/structs` + GUI settings.
- [ ] **P3.6** Wire **slow path** in `jarvis-app` main loop: on `NeedsLlm`, call facade, then **tool loop** until terminal message.

---

## Phase 4 — Tool dispatcher & safety (Arch 7, principle 8)

Minimal tools; map to existing execution.

- [ ] **P4.1** Register **tools** with short JSON schemas: e.g. `run_command` (command id + args), `play_reaction` (enum → `voices::Reaction`), `list_commands` / `search_commands` (paginated or query).
- [ ] **P4.2** Implement **dispatcher** in `jarvis-app` (or core): map tool name → typed handler; return tool results to the LLM in the next chat turn.
- [ ] **P4.3** **Safety:** disallow arbitrary shell from tools by default; only **manifested** command ids or Lua entrypoints; add **allowlist** or user confirmation for high-risk actions (iterative).
- [ ] **P4.4** **System prompt**: single short template file or const; inject only dynamic context (language, time) in user message.

---

## Phase 5 — Voice provisioning & optional live TTS (Arch 8)

Bake workflow + future runtime TTS.

- [ ] **P5.1** Specify **`voice.manifest.yaml`** schema (reaction, locale, text, output basename) and add **one example** pack manifest in `resources/sound/voices/`.
- [ ] **P5.2** Add **`scripts/voice-bake/`** (Python or Node): read manifest + `voice.toml`, call pluggable TTS driver (OpenAI TTS, Piper CLI, etc.), write clips; optional **`provenance.toml`** output.
- [ ] **P5.3** Document **bake** workflow in README or `design/ARCHITECTURE.md` (link from this roadmap).
- [ ] **P5.4** *(Optional)* **Tier B** disk cache: keyed by `(voice_pack, lang, text_hash)` for fixed strings without clips.
- [ ] **P5.5** *(Optional)* **Tier C** long-running **TTS sidecar** + settings (host, port, persona → model); integrate only for dynamic/LLM text.

---

## Phase 6 — Platform & polish

- [ ] **P6.1** **macOS tray**: implement or document supported alternative (menu bar, GUI-only control).
- [ ] **P6.2** Resolve or document **`TODO`** / fixme items in `jarvis-app`, `listener/rustpotter`, `commands`, `recorder` (configurability, security notes).
- [ ] **P6.3** **OpenAI API key** in settings: either wire to LLM/TTS bake or remove dead UI strings.

---

## Phase 7 — Differentiation backlog (Arch 13)

Not required for parity with the doc, but tracks competitive goals.

- [ ] **P7.1** Installer or **dev setup script** for **llama-server** / model download (per OS), inspired by novik’s “bundled server” UX but cross-platform where feasible.
- [ ] **P7.2** Optional **system stats** surface in GUI (IPC or invoke) — lightweight answer to KDE widget monitoring.
- [ ] **P7.3** **Capability tiers** for LLM-exposed tools (user consent levels).

---

## Suggested order

```text
P0 → P1 → P2 → P3 (HTTP first) → P4 → P5 (manifest + baker) → P6 → P7
```

**Critical path to “architecture-complete” for LLM/tooling (Arch 7):** **P2** + **P3** + **P4**.  
**Critical path for voice bake story (Arch 8):** **P5.1–P5.3**.

---

## Traceability

| Phase | Primary `ARCHITECTURE.md` sections |
|-------|-----------------------------------|
| P0 | Doc hygiene, section 10 |
| P1 | 4, 12 |
| P2 | 6–7 |
| P3 | 7, principles 3–4 (section 2) |
| P4 | 7, principle 8 (section 2) |
| P5 | 8 |
| P6 | 12, tray (section 4) |
| P7 | 13 |

---

*Revise this file when phases complete or scope changes.*
