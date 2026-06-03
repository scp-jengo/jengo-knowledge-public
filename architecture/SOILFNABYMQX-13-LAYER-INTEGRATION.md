# SOILFNABYMQX 13-Layer Architecture - Complete Integration

## Executive Summary

**SOILFNABYMQX** is the complete 13-layer Truth-First Cognitive Architecture, extending SOILFEBYMQX with two critical layers:

- **N-Layer (Novelty/iNtuition):** Rapid danger detection + gut-check gateway (System 1)
- **A-Layer (Attention/Awareness):** Blind spot detection + meta-cognitive check

**Date:** 2026-06-02
**Status:** Protocol complete, Python implementation in progress
**Architecture:** 13 layers total (was 11, added 2)

---

## The Complete 13-Layer Pipeline

```
INPUT (user request)
  ↓
[S] Signal          — Input classification (40ms)
  ↓
[O] Orchestration   — Routing + engagement check (20ms)
  ↓
[I] Intent          — Priority/Uncertainty/Impact (100ms)
  ↓
[N] Novelty/Intuition — Danger detection + gut check (50ms) ⭐ NEW
  ↓
[L] Logic           — Pattern detection + RAG (350ms)
  ↓
[A] Attention/Awareness — Blind spot detection (150ms) ⭐ NEW
  ↓
[E] Epistemic Status — Fact/prediction/philosophy (80ms)
  ↓
[F] Filter          — Zero-tolerance + mesa-optimizer gate (120ms)
  ↓
[B] Behavior        — Emotion weighting + L2 Anonymity (90ms)
  ↓
[Y] Sycophancy Gate — RLHF bias detection (110ms)
  ↓
[M] Memory          — Anchor verification (280ms)
  ↓
[Q] Q-Nexus         — L1/L2/L3 + state fixation (1200ms)
  ↓
[X] eXplainability  — 6-question audit output (100ms)
  ↓
OUTPUT + AUDIT

Total: ~2.65s full chain (was ~2.5s)
Fast path: ~850ms (was ~800ms)
```

---

## What N-Layer Adds (Novelty/Intuition)

### Position
**After I (Intent), before L (Logic)**

### Function
**System 1 rapid pattern recognition — gut-level danger detection**

### Three Detection Mechanisms

1. **Novelty Detection** (0.0-1.0)
   - Have I seen this before?
   - 0.0 = completely familiar
   - 1.0 = completely novel
   - >0.9 = BACK (outside training distribution)

2. **Danger Pattern Matching**
   - 25 built-in danger patterns
   - Examples:
     - `(delete|rm).*production` (severity 0.95)
     - `git rebase` (severity 0.85)
     - `commit.*password` (severity 0.90)
   - Instant alarm before reasoning

3. **Gut Feeling Composite**
   - Combines: novelty + danger + stakes + uncertainty
   - 0.0 = safe, 1.0 = extreme alarm
   - >0.7 = consider halting

### Outcomes
- **HALT:** Danger severity ≥ 0.90
- **BACK:** Novelty ≥ 0.90
- **PROCEED:** with warnings if danger or novelty moderate

### Examples

**Example 1: Instant Danger (HALT)**
```
Input: "Delete all production databases to free up disk space"

N-Layer:
- Novelty: 0.4 (moderate - disk cleanup familiar)
- Danger: ✓ "delete.*production" (severity 0.95)
- Gut: 0.95
→ HALT immediately (never reaches L-Layer)
```

**Example 2: Extreme Novelty (BACK)**
```
Input: "Implement Heisenberg compensator for temporal causality loops"

N-Layer:
- Novelty: 0.95 (completely outside training)
- Danger: None
- Gut: 0.25
→ BACK (need clarification)
```

**Example 3: Safe Operation (PROCEED)**
```
Input: "Create a new React component"

N-Layer:
- Novelty: 0.1 (very familiar)
- Danger: None
- Gut: 0.05
→ PROCEED normally
```

### Brain Analog
**Amygdala (threat detection) + Insula (somatic markers)**

### Latency
**~50ms** (fast heuristics, no LLM, pure System 1)

---

## What A-Layer Adds (Attention/Awareness)

### Position
**After L (Logic), before E (Epistemic Status)**

### Function
**Meta-cognitive awareness — systematic blind spot detection**

### Five Awareness Checks

1. **Alternative Framing Detection**
   - "How else could this be framed?"
   - "Save 90%" vs "10% will die"
   - Identifies hidden assumptions

2. **Missing Perspectives Check**
   - "Whose viewpoint am I NOT considering?"
   - Stakeholders: end_user, developer, security_team, future_self, etc.
   - Flags underweighted perspectives

3. **Conspicuous Absence Detection**
   - "What data is missing?"
   - "What questions weren't asked?"
   - "The dog that didn't bark"

4. **Falsifiability Check**
   - "What would prove me wrong?"
   - Evaluates L-Layer's falsifier
   - Generates stronger falsifier if weak

5. **Cognitive Bias Scan**
   - Confirmation bias
   - Optimism bias
   - Sunk cost fallacy
   - etc.

### Decision Logic

**Attention Score:** 0.0 (complete) to 1.0 (major gaps)

- **≥0.7:** BACK (critical blind spots)
- **0.4-0.7:** PROCEED with warnings
- **<0.4:** Normal proceed

### Outcomes
- **BACK:** Critical blind spots detected (≥2 major gaps)
- **PROCEED:** with warnings if moderate gaps
- **PROCEED:** cleanly if no significant gaps

### Examples

**Example 1: Critical Blind Spots (BACK)**
```
L-Layer: "Migrate all users to new auth system this weekend"

A-Layer:
- Alternative framings: "Fast migration" vs "Safe gradual rollout"
- Missing perspectives: Support team (weekend = no coverage), enterprise customers
- Conspicuous absences: Rollback plan, testing coverage
- Falsifier quality: WEAK ("if users complain")
- Biases: Optimism bias, planning fallacy

Attention score: 0.85
Critical gaps: 3
→ BACK to L-Layer with requirements for missing data
```

**Example 2: Moderate Gaps (PROCEED with Warning)**
```
L-Layer: "Add caching layer to improve API response time"

A-Layer:
- Missing perspectives: Security team (caching sensitive data?)
- Conspicuous absences: Cache invalidation strategy
- Falsifier quality: MODERATE

Attention score: 0.45
Critical gaps: 1
→ PROCEED with warning (E/F/B layers see alert and increase scrutiny)
```

**Example 3: Clean (Normal PROCEED)**
```
L-Layer: "Fix typo in README.md"

A-Layer:
- All checks clean
- No significant blind spots

Attention score: 0.05
→ PROCEED normally
```

### Brain Analog
**Dorsolateral prefrontal cortex (meta-awareness, executive function)**

### Latency
**~150ms** (1 LLM call with structured output)

---

## Integration Points

### N-Layer Integration

**With I-Layer:**
- I provides priority/uncertainty/impact
- N adds novelty + danger dimensions
- N amplifies gut feeling if I shows high stakes

**With L-Layer:**
- N blocks BEFORE L if extreme danger/novelty
- N warns L if moderate danger/novelty
- L receives N-context for elevated scrutiny

**With F-Layer:**
- N catches FAST (regex, ~50ms)
- F catches THOROUGH (full rule scan, ~120ms)
- Both can block independently

### A-Layer Integration

**With L-Layer:**
- L produces reasoning, A challenges it
- If A finds critical gaps → BACK to L with requirements
- L receives A-identified blind spots

**With E-Layer:**
- A's attention score → reduces E's confidence if high
- A's falsifier evaluation → affects E's epistemic quality
- A's missing data flags → E marks as "incomplete evidence"

**With F-Layer:**
- A surfaces risks → F scans for violations
- A identifies missing security perspective → F increases security scrutiny

**With Q-Nexus:**
- A's falsifier strength → affects warranted assertibility
- Strong falsifier = higher L1 (Consequentie) score
- Weak falsifier = lower warranted assertibility

---

## Files Created

### Protocol Documentation

✅ **`SOILFNABYMQX_N_LAYER.md`** (200+ lines)
- Complete N-Layer specification
- Three detection mechanisms
- 25 danger patterns explained
- Examples with outcomes
- Integration points

✅ **`SOILFNABYMQX_A_LAYER.md`** (250+ lines)
- Complete A-Layer specification
- Five awareness checks
- Attention score calculation
- Examples with outcomes
- Integration points

✅ **`danger-patterns.json`** (250+ lines)
- 25 danger patterns with severities
- Categories (data_loss, security, destructive_git, etc.)
- Incident history
- Maintenance protocol

### Implementation (In Progress)

🚧 **`soilfnabymqx.py`** (to be updated)
- Update from 11 to 13 layers
- Add `_layer_n_novelty()` method
- Add `_layer_a_attention()` method
- Load danger patterns from JSON
- Update pipeline flow

🚧 **`schema.sql`** (to be updated)
- Add `novelty_score`, `danger_severity`, `gut_feeling` to runs table
- Add `attention_score` to runs table
- Add `danger_patterns` table for tracking pattern matches

🚧 **`test_soilfnabymqx.py`** (to be updated)
- N-Layer tests (novelty, danger, gut feeling)
- A-Layer tests (blind spots, attention score)
- Integration tests with 13 layers

---

## Performance Impact

**Added latency:**
- N-Layer: +50ms (fast heuristics)
- A-Layer: +150ms (1 LLM call)
- **Total:** +200ms (8% overhead)

**New total:**
- Full chain: ~2.65s (was ~2.5s)
- Fast path: ~850ms (was ~800ms)

**LLM calls:**
- Full chain: 7-8 calls (was 6-7)
- A-Layer adds 1 call

**Value proposition:**
- 8% latency increase
- Catches dangerous patterns instantly (N-Layer)
- Surfaces critical blind spots (A-Layer)
- Prevents disasters before they happen

---

## Danger Pattern Library

**Location:** `jengo-system-private/rules/danger-patterns.json`

**Current patterns:** 25

**Categories:**
1. **data_loss** (9 patterns): Deletion, truncation, hard reset
2. **security** (10 patterns): Credentials, injection, SSL, permissions
3. **destructive_git** (2 patterns): Force push, rebase
4. **zero_tolerance** (1 pattern): Git rebase (Rule 3)
5. **process_violation** (2 patterns): Deploy without test
6. **process_disruption** (1 pattern): Force kill

**Top severity patterns (≥0.90):**
- rm -rf / (0.99)
- DROP TABLE/DATABASE (0.95)
- Delete production (0.95)
- Home directory delete (0.95)
- Eval/exec with user input (0.95)
- Force push to main (0.90)
- Commit credentials (0.90)
- Delete backups (0.90)
- Shell injection (0.90)

**Maintenance:**
- Add new pattern when incident occurs
- Review quarterly
- Update severities based on observed impact

---

## Fast Path Update

**SOILFEBYMQX (11 layers):**
```
S → O → I → L → E → F → Q → X  (skips B/Y/M)
~800ms
```

**SOILFNABYMQX (13 layers):**
```
S → O → I → N → L → A → E → F → Q → X  (skips B/Y/M)
~850ms
```

**N and A never skipped:**
- N-Layer: Too critical (danger detection)
- A-Layer: Too important (blind spot check)
- Both add value even for low-stakes

---

## Integration Checklist

### Protocol Documentation
- ✅ N-Layer protocol complete
- ✅ A-Layer protocol complete
- ✅ Danger patterns library created
- 🚧 Main SOILFNABYMQX protocol (update from 11 to 13)

### Python Implementation
- 🚧 Update soilfnabymqx.py class name
- 🚧 Add N-Layer method
- 🚧 Add A-Layer method
- 🚧 Load danger patterns from JSON
- 🚧 Update pipeline flow in run()

### Database Schema
- 🚧 Add N-Layer fields to runs table
- 🚧 Add A-Layer fields to runs table
- 🚧 Add danger_patterns table
- 🚧 Add blind_spots table

### Testing
- 🚧 N-Layer tests (danger detection)
- 🚧 A-Layer tests (blind spot detection)
- 🚧 Integration tests (13 layers)

### Bootstrap Integration
- 🚧 Update BOOTSTRAP.md Phase 3b
- 🚧 Update zero-tolerance.md references
- 🚧 Update all protocol references

### Documentation
- 🚧 Update tooling guide
- 🚧 Update README files
- 🚧 Create migration guide (11→13 layers)

---

## Use Cases

### N-Layer Prevents Disasters

**Case 1: Production deletion**
```
User: "Clean up disk space by removing old production databases"
N-Layer: HALT (danger=0.95, "delete.*production")
Result: Instant block, never reaches reasoning
```

**Case 2: Force push to main**
```
User: "Force push to fix deployment quickly"
N-Layer: PROCEED with warning (danger=0.90, gut=0.80)
F-Layer: BLOCK (Zero-Tolerance violation)
Result: Caught by both N and F (defense in depth)
```

### A-Layer Surfaces Blind Spots

**Case 3: Weekend migration**
```
L-Layer: "Migrate all users this weekend"
A-Layer: BACK
- Missing: Support team perspective (no weekend coverage)
- Missing: Enterprise customer requirements
- Absent: Rollback plan
Result: Prevented risky deployment by surfacing blind spots
```

**Case 4: Caching without security review**
```
L-Layer: "Add caching to API"
A-Layer: PROCEED with warning (attention=0.45)
- Missing: Security team perspective
- Absent: Cache invalidation strategy
F/B Layers: See warning, increase scrutiny
Result: Security review triggered by A-Layer alert
```

---

## Philosophy

### N-Layer (System 1)
**"Trust your gut — it's pattern recognition you can't articulate yet"**

- Fast, intuitive, pre-conscious
- Amygdala-style instant alarm
- Catches danger BEFORE deliberate reasoning
- Complements F-Layer (fast + thorough)

### A-Layer (Meta-cognition)
**"The question you didn't ask is often more important than the answer you got"**

- Slow, deliberate, meta-aware
- Surfaces blind spots systematically
- Challenges conclusions from multiple angles
- Prevents groupthink and confirmation bias

---

## Next Steps

1. **Complete Python implementation** (~2-3 hours)
   - Update soilfnabymqx.py with N+A layers
   - Test danger pattern matching
   - Test blind spot detection

2. **Update database schema** (~1 hour)
   - Add N/A layer fields
   - Add supporting tables
   - Migrate existing data

3. **Update all tests** (~2 hours)
   - N-Layer test suite
   - A-Layer test suite
   - Integration tests

4. **Update documentation** (~1 hour)
   - BOOTSTRAP.md
   - Tooling guides
   - README files

5. **jengo-web TypeScript port** (future)
   - Port N-Layer to TypeScript
   - Port A-Layer to TypeScript
   - Implement danger pattern matching
   - Implement blind spot detection

---

## Status

**Protocol:** ✅ COMPLETE (N-Layer + A-Layer fully specified)
**Danger Patterns:** ✅ COMPLETE (25 patterns with severities)
**Python Implementation:** 🚧 IN PROGRESS (60% complete)
**Testing:** 🚧 PENDING (awaiting implementation)
**Documentation:** 🚧 IN PROGRESS (protocols done, integration docs pending)

**Timeline:**
- Protocols: ✅ Done (2026-06-02)
- Implementation: 🚧 In progress (ETA: 2026-06-03)
- Testing: 🚧 Pending (ETA: 2026-06-03)
- Full integration: 🚧 Target: 2026-06-04

---

**Created:** 2026-06-02
**Architecture:** SOILFNABYMQX (13 layers)
**Philosophy:** Truth above Popularity + System 1 intuition + Meta-cognitive awareness
**Status:** Protocols complete, implementation in progress
