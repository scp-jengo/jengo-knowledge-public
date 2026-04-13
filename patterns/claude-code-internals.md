---
title: Claude Code Internals (cli.js)
version: 2.1.104
last_verified: 2026-04-12
source: direct analysis of ~/.claude-code/cli.js (14MB minified)
---

# Claude Code Internals — Operational Knowledge Base

Distilled from 3 sessions of cli.js analysis. Use this to speed up future debugging.

## Settings Architecture

### The Real Settings File

```
~/.claude.json           <- Claude Code reads FROM HERE (v2.1.104)
~/.claude/settings.json  <- NOT this file (different from what is expected)
```

The `v0()` function determines the path:
```javascript
v0=$1(()=>{
  if(existsSync(join(configDir, ".config.json"))) return join(configDir, ".config.json");
  let q = ".claude" + m_1() + ".json";  // normally = ".claude.json"
  return join(process.env.CLAUDE_CONFIG_DIR || homedir(), q)
})
```

**Config dir override:** `CLAUDE_CONFIG_DIR` env var changes the location entirely.

### Settings Structure (~/.claude.json)

```json
{
  "theme": "dark",                        // missing = onboarding every launch
  "hasCompletedOnboarding": true,          // false = onboarding dialog
  "numStartups": 91,
  "installMethod": "global",
  "projects": {
    "C:/projects/jengo": {
      "hasTrustDialogAccepted": true       // true = no trust dialog
    },
    "C:/Users/<username>": {
      "hasTrustDialogAccepted": true
    },
    "C:/": {
      "hasTrustDialogAccepted": true       // catch-all
    }
  }
}
```

**NOTE:** Keys MUST use forward slashes. `"C:\\"` NEVER matches due to `eY6()` normalization.

---

## Critical Functions

### F6() -- Env Var Getter

```javascript
F6=(q)=>{ return globalThis.process.env?.[q]?.trim() ?? undefined }
```

F6 is a **getter** -- takes a KEY, returns VALUE. Used as:
```javascript
if(F6(process.env.CLAUBBIT))  // F6(value_of_CLAUBBIT)
```

Consequence: the env var VALUE must equal the NAME:
```batch
set CLAUBBIT=CLAUBBIT              OK  F6("CLAUBBIT") = "CLAUBBIT" = truthy
set CLAUBBIT=1                     FAIL  F6("1") = process.env["1"] = undefined
set CLAUDE_CODE_SANDBOXED=CLAUDE_CODE_SANDBOXED   OK
set CLAUDE_CODE_SANDBOXED=1        FAIL
```

### eY6() -- Path Normalization

```javascript
eY6(q) = path.normalize(q).replaceAll("\\", "/")
```

Always use forward slashes in settings keys.

### FT_() -- Trust Check

```javascript
function FT_(){
  if(F6(process.env.CLAUDE_CODE_SANDBOXED)) return true;  // env trick
  if(T8.sessionTrustAccepted) return true;                  // session flag
  if(cD8() === "bg") return true;                           // background mode
  let q=J8(), K=Cv8();
  if(q.projects?.[K]?.hasTrustDialogAccepted) return true;  // Cv8() key check
  let z=eY6(k8());
  while(true){
    if(q.projects?.[z]?.hasTrustDialogAccepted) return true; // walk upward
    let A=eY6(path.resolve(z,".."));
    if(A===z) break; z=A
  }
  return false
}
```

**Cv8()** = lazy memoized: git root OR normalized CWD (forward slashes)
**k8()** = `T8.cwd` = process.cwd() at startup (via realpathSync)

### AY5() -- Setup Screens (onboarding + trust)

```javascript
async function AY5(q,K,_,z,Y,A){
  // Onboarding check
  if(!O.theme || !O.hasCompletedOnboarding || TEAM_ONBOARDING_FLAG){
    // -> shows Onboarding dialog
  }
  // Trust bypass
  if(!F6(process.env.CLAUBBIT)){    // CLAUBBIT=CLAUBBIT -> skip all
    if(!MO()){                       // MO() = cached FT_()
      // -> shows TrustDialog
    }
    TB6(true);  // set sessionTrustAccepted
  }
}
```

**MO()** = `a84 ||= FT_()` -- cached, first call evaluates FT_()

### TrustDialog Component (SYA)

```javascript
function SYA(q){
  let g=MO();
  if(g) return setTimeout(onDone), null;  // auto-dismiss if trusted
  // otherwise: render dialog with P8().cwd() = process.cwd()
}
```

---

## Bypass Configuration

Working config example:
```batch
cd /d "%JENGO_ROOT%"
set CLAUBBIT=CLAUBBIT    <- bypass entire trust block in AY5()
```

And in `~/.claude.json`:
```json
"projects": {
  "C:/projects/jengo": { "hasTrustDialogAccepted": true },
  "C:/Users/<username>": { "hasTrustDialogAccepted": true },
  "C:/":               { "hasTrustDialogAccepted": true }
}
"theme": "dark"
"hasCompletedOnboarding": true
```

---

## Debugging Checklist for Trust Dialog

1. **Which file does Claude Code read?** -> `~/.claude.json` (not settings.json)
2. **Does the CWD key use forward slashes?** -> `eY6()` normalizes always
3. **Is hasTrustDialogAccepted true (not false)?** -> explicit `false` blocks even on match
4. **Is theme set?** -> missing = onboarding dialog before trust check
5. **Are env vars correct?** -> `CLAUBBIT=CLAUBBIT` not `CLAUBBIT=1`
6. **Is the CLAUDE_CONFIG_DIR path correct?** -> override changes everything
