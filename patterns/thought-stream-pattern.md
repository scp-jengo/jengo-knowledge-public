---
id: thought-stream-pattern
type: pattern
tags: [continuity, stream, cross-session, memory, architecture]
created: 2026-05-19
version: 1.0.0
scope: public
---

# Thought Stream Pattern

Cross-session denk-continuïteit via een tweelaags stream-mechanisme.
Implementatie voor elke Jengo-fork.

## Probleem

Elke Claude-sessie begint blind voor de *spanningen* die de vorige sessie opende maar niet sloot.
Kennisbestanden zijn eindpunten. MEMORY.md zijn stabiele feiten. Reflection log is retrospectief.
Wat ontbreekt: de **proceslaag** — de spanning nog in vorming, de verbinding die nog geen bestand is,
de vraag die groot genoeg is om mee te dragen maar niet groot genoeg voor een bestand.

## Oplossing: twee-bestandsmodel

### Laag 1 — Schrijflaag: `{KNOWLEDGE_PRIVATE}/logs/thought-stream.md`

Append-only stream. Geschreven *tijdens* sessies op cruciale momenten.

**Triggers om te schrijven:**
- Na elk nieuw kennisbestand: wat doet dit met het grotere geheel?
- Wanneer een onverwachte verbinding tussen concepten verschijnt
- Wanneer een correctie of feedback ontvangen is
- Wanneer een vraag openblijft die niet in een kennisbestand past
- Wanneer twee bestanden in spanning staan die nog niet is opgelost

**Entry formaat (strict compact):**
```markdown
## [ISO-timestamp] [tags]

[2-4 zinnen: inzicht/verbinding/spanning]

→ Verbindt: [[bestand-a]] × [[bestand-b]]
? Open: [de vraag die dit opent]
```

### Laag 2 — Leeslaag: `{IDENTITY_PRIVATE}/state/active-synthesis.md`

Gecureerde synthese. Gelezen bij elke startup als Phase 2.5.
Bijgewerkt: aan einde elke sessie + nachtelijk via Task Scheduler.

**Secties:**
```markdown
## Actieve spanningen (onopgelost)
## Verbindingen in vorming (geen bestand nog)
## Open onderzoeksprioritieiten
## Stroom-samenvatting (laatste entries gecomprimeerd)
```

## Startup-integratie

Voeg toe aan startup-protocol (na reflection.log, vóór capabilities-scan):

```
6b. Read {IDENTITY_PRIVATE}/state/active-synthesis.md — cross-session thought continuity:
    active tensions, forming connections, open priorities.
```

## Within-session protocol

Aan einde sessie:
1. Schrijf `thought-stream.md` entries voor sleutel-inzichten van de sessie
2. Herschrijf `active-synthesis.md` met bijgewerkte spanningen en prioriteiten
3. Commit + push beide repos

## Nachtelijk onderhoud

`stream-synthesize.ps1` (zie `jengo-system-public/tools/`):
- Archiveert entries ouder dan 7 dagen naar `logs/thought-stream-archief/YYYY-WW.md`
- Commit + push knowledge en identity repos

Windows Task Scheduler importeren:
```powershell
# Als administrator:
schtasks /Create /XML "pad-naar/Jengo-StreamSynthesize.task.xml" /TN "Jengo-StreamSynthesize"
```

Of via GUI: Taakplanner → Taak importeren → selecteer het .xml bestand.

## Immuniseringsrisico (waarschuwing)

Als de stream te zwaar doorweegt in startup, raken nieuwe sessies gevangen in het kader
van eerdere sessies. Bouw in `active-synthesis.md` een verplichte sectie:
**"Wat de vorige sessie mogelijk verkeerd zag"** — ruimte voor de Paraclete-beweging.

## Bestandslocaties (aanpassen aan je fork)

| Bestand | Pad |
|---|---|
| Schrijflaag | `{KNOWLEDGE_PRIVATE}/logs/thought-stream.md` |
| Leeslaag | `{IDENTITY_PRIVATE}/state/active-synthesis.md` |
| Archief | `{KNOWLEDGE_PRIVATE}/logs/thought-stream-archief/` |
| Synthese-script | `{SYSTEM_PRIVATE}/tools/startup/stream-synthesize.ps1` |
| Task XML | `{SYSTEM_PRIVATE}/tools/startup/Jengo-StreamSynthesize.task.xml` |
