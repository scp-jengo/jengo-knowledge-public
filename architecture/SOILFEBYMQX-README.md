# SOILFEBYMQX Architecture Integration

## Overview

**SOILFEBYMQX** is the complete 11-layer cognitive processing pipeline integrated from the Bugatti Platform "Truth-First Cognitive Architecture" into Jengo's SCP (Synthetic Cognitive Platform).

**Date Integrated:** 2026-06-02
**Source:** Bugatti Platform SOILFBMQX diagrams + Jengo SOLFEBYMQ protocol

---

## The 11 Layers

```
S → O → I → L → E → F → B → Y → M → Q → X
```

| # | Layer | Function | Type | Latency | Added |
|---|-------|----------|------|---------|-------|
| 1 | **S** Signal | Input classification + substrate declaration | Code | 40ms | 2026-04-18 |
| 2 | **O** Orchestration | Routing + engagement verification | Code | 20ms | 2026-04-18 |
| 3 | **I** Intent | Priority/Uncertainty/Impact heat analysis | Hybrid | 100ms | **2026-06-02** |
| 4 | **L** Logic | Pattern detection + RAG retrieval | LLM | 350ms | 2026-04-18 |
| 5 | **E** Epistemic Status | Fact/prediction/philosophy classification | LLM | 80ms | 2026-05-28 |
| 6 | **F** Filter | Quality gate + mesa-optimizer detection | Hybrid | 120ms | 2026-04-18 |
| 7 | **B** Behavior | Emotion weighting + L2 Anonymity Gate | Hybrid | 90ms | 2026-04-20 |
| 8 | **Y** Sycophancy Gate | RLHF bias detection + facts-over-validation | LLM | 110ms | 2026-05-28 |
| 9 | **M** Memory | Anchor verification + signal coherence check | Hybrid | 280ms | 2026-04-18 |
| 10 | **Q** Q-Nexus | L1/L2/L3 warranted assertibility + state fixation | LLM | 1200ms | 2026-04-18 |
| 11 | **X** eXplainability | 6-question audit trail + transparency output | Hybrid | 100ms | **2026-06-02** |

**Total:** ~2.5s full chain | ~0.8s fast path (S→O→I→L→E→F→Q→X)

---

## New Layers (Bugatti Integration)

### I-Layer: Intent (Priority Engine)

**Position:** After Orchestration, before Logic

**Function:** Pre-reasoning filter that assesses:
1. **Priority Heat** (0.0-1.0): Urgency level
2. **Uncertainty Heat** (0.0-1.0): Ambiguity level
3. **Impact Heat** (0.0-1.0): Blast radius

**Feeds into:**
- ACC Emotion-Ware Relevance Field
- B-Layer Stakes assessment
- Fast path eligibility decision

**Fast Path Trigger:** If Priority < 0.3 AND Uncertainty < 0.3 AND Impact < 0.3 → skip B/Y/M layers

**Protocol:** `jengo-system-private/protocols/SOILFEBYMQX_I_LAYER.md`

---

### X-Layer: eXplainability (Output Accountability)

**Position:** After Q-Nexus, before final output

**Function:** Transform Q-fixed state into transparent, accountable output

**Six Mandatory Questions:**
1. **Waarom dit antwoord?** (Why this answer?) — Reasoning chain
2. **Welke bronnen gebruikt?** (Which sources?) — Complete attribution
3. **Wat zijn de trade-offs?** (Trade-offs?) — Optimizes for/sacrifices
4. **Wat is de zekerheid?** (Certainty?) — Confidence breakdown
5. **Wat was de redenering?** (Reasoning?) — Layer-by-layer trace
6. **Volledige audit trail (ID)?** (Audit trail?) — Storage location + retrieval

**Output Formats:**
- Human-readable: Markdown for user display
- Machine-readable: JSON for audit database

**Dual Storage:**
- SQLite: `jengo-knowledge-private/logs/soilfebymqx-audit.db` (queryable, 90-day retention)
- Log file: `jengo-knowledge-private/logs/soilfebymqx-audit.log` (append-only, permanent)

**Protocol:** `jengo-system-private/protocols/SOILFEBYMQX_X_LAYER.md`

---

## Evolution Timeline

| Date | Version | Layers | Change |
|------|---------|--------|--------|
| 2026-04-18 | SOLFMQ | 7 | Original pipeline |
| 2026-04-20 | SOLFBMQ | 7 | B-Layer added (Behavior/Damasio) |
| 2026-05-28 | SOLFEBYMQ | 9 | E-Layer (Epistemic Status) + Y-Layer (Sycophancy Gate) |
| 2026-06-02 | **SOILFEBYMQX** | **11** | **I-Layer (Intent) + X-Layer (eXplainability)** |

---

## Design Principles

**Jengo (Schepman Doctrine):**
> "Not the biggest, not the fastest, but the AI that's best efficient by effectiveness."

**Bugatti Platform:**
> "Waarheid boven Populariteit" (Truth above Popularity)

Both architectures prioritize **correctness over speed**, **truth over convenience**.

---

## Architecture Diagrams

![SOILFEBYMQX Full Architecture](SOILFEBYMQX.jpg)

Full diagram showing:
- 11-layer pipeline
- Dual-system cognition (System 1: Reason/Logic, System 2: Rule/Context)
- Emotion-Ware Relevance Field
- Register architecture (Event Sourcing)
- 3 Core Priorities (Betrouwbaarheid, Effectiviteit, Efficiëntie)

![SOILFEBYMQX Organizational View](SOILFEBYMQX-org.jpg)

Organizational diagram showing:
- Intent Layer as Priority Engine
- System 2 integration (SOI layer as inhibitor)
- Register architecture detail
- X-Layer output format

---

## Files Modified (Integration)

### jengo-system-private
- ✅ `protocols/SOILFEBYMQX_REASONING_CHAIN.md` — Complete 11-layer spec (NEW)
- ✅ `protocols/SOILFEBYMQX_I_LAYER.md` — Intent Layer spec (NEW)
- ✅ `protocols/SOILFEBYMQX_X_LAYER.md` — eXplainability Layer spec (NEW)
- ✅ `rules/zero-tolerance.md` — Updated references to SOILFEBYMQX

### jengo-identity-machine
- ✅ `BOOTSTRAP.md` — Updated Phase 3b to reference SOILFEBYMQX 11-layer chain

### jengo-web
- ✅ `docs/solfbmq-pipeline-plan.html` — Updated to SOILFEBYMQX with I/X layers

### jengo-knowledge-public
- ✅ `architecture/SOILFEBYMQX.jpg` — Bugatti diagram (copied)
- ✅ `architecture/SOILFEBYMQX-org.jpg` — Organizational diagram (copied)
- ✅ `architecture/SOILFEBYMQX-README.md` — This file (NEW)

---

## Implementation Status

### Protocols: ✅ COMPLETE
- All 11 layers documented
- I-Layer and X-Layer specs created
- Main SOILFEBYMQX protocol comprehensive

### Bootstrap Integration: ✅ COMPLETE
- BOOTSTRAP.md references SOILFEBYMQX
- Zero-tolerance rules updated
- Full protocol paths declared

### jengo-web Implementation: 🚧 PENDING
- Phase 0: Scaffolding (11-layer stubs) — NOT STARTED
- Target: First production SOILFEBYMQX implementation
- Endpoint: `POST /api/soilfebymqx`

### LangGraph Templates: 🚧 NEEDS UPDATE
- Current: 7-layer templates (pre-E/Y/I/X)
- Target: 11-layer templates
- Files: `jengo-system-private/templates/solfbmq-harness.js`, `test-solfbmq-harness.js`

---

## Fast Path Logic

**Enabled by I-Layer:** Intelligent shortcuts for low-stakes requests

**Conditions:**
- Priority Heat < 0.3 (LOW)
- Uncertainty Heat < 0.3 (CLEAR)
- Impact Heat < 0.3 (LOCAL)
- L-Layer confidence > 0.8
- No Zero-Tolerance triggers

**Pipeline:** S→O→I→L→E→F→Q→X (skips B/Y/M)

**Latency:** ~800ms vs ~2500ms full chain

**Examples:**
- "What's the current branch?" ✅ Fast path
- "List TODO agents" ✅ Fast path
- "Deploy to production" ❌ Full chain (high impact)
- "Fix auth bug" ❌ Full chain (high uncertainty)

---

## Integration with Five-Principle Meta-Layer

SOILFEBYMQX enforces all 5 principles at Q-Nexus:

1. **L1-without-L2 Detection** → F-Layer + B-Layer
2. **Signal Integration Health** → M-Layer
3. **L1-Theater Detection** → Y-Layer
4. **Substrate Literacy** → S-Layer + L-Layer + E-Layer
5. **Engagement Requirement** → O-Layer + I-Layer

**Q-Nexus blocks if ANY principle fails.**

---

## Example Use Cases (Bugatti)

### Fromanger Case (Conflict Litigation)
- **I-Layer:** Priority=0.8, Uncertainty=0.5, Impact=0.9 → Full chain
- **F-Layer:** Zero-tolerance check (legal accuracy)
- **B-Layer:** Anonymity Check (high stakes)
- **Q-Nexus:** L1/L2/L3 all pass
- **X-Layer:** Complete provenance trail with source citations

### Deanice Bugatti ("Wrong Definition 1922")
- **I-Layer:** Priority=0.6, Uncertainty=0.3, Impact=0.7 → Full chain
- **F-Layer:** Anchor conflict check (historical accuracy)
- **M-Layer:** Multiple corroborating sources required
- **Q-Nexus:** L1 (measurement) + L2 (would correct even if unpopular) + L3 (survives peer review)
- **X-Layer:** Trade-offs: corrects misconception vs. contradicts popular belief

---

## References

**Protocol Files:**
- `jengo-system-private/protocols/SOILFEBYMQX_REASONING_CHAIN.md`
- `jengo-system-private/protocols/SOILFEBYMQX_I_LAYER.md`
- `jengo-system-private/protocols/SOILFEBYMQX_X_LAYER.md`
- `jengo-system-private/protocols/SOLFBMQ_B_LAYER.md`

**Bootstrap:**
- `jengo-identity-machine/BOOTSTRAP.md` (lines 61-95)

**Implementation Plan:**
- `jengo-web/docs/solfbmq-pipeline-plan.html` (updated 2026-06-02)

**Diagrams:**
- `jengo-knowledge-public/architecture/SOILFEBYMQX.jpg`
- `jengo-knowledge-public/architecture/SOILFEBYMQX-org.jpg`

---

**Status:** INTEGRATED (2026-06-02)
**Next:** jengo-web Phase 0 implementation (11-layer scaffolding)
**Philosophy:** Waarheid boven Populariteit — Truth-First Cognitive Architecture
