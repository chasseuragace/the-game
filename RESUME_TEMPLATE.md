# 🎮 ACTIVE GAME STATE

**The Game No One Has Completed**  
**Version:** 2.1 | **Status:** Ready

---

## PLAYER

| Field | Value |
|-------|-------|
| **Build** | _None equipped_ |
| **Tier** | - |
| **Trust** | - |
| **Mindstate** | _Not loaded_ |
| **Location** | _Not set_ |
| **Session** | 1 |

---

## COGNITIVE STATE

| Field | Value |
|-------|-------|
| **MS State** | _Not tracked_ |
| **Confidence** | - |
| **Since turn** | - |
| **Blend** | - |

**Trajectory this session:**
```
(no states recorded yet)
```

**Last transition:**
- From: -
- To: -
- Trigger: -
- Turn: -

---

## CONTEXT

**Working on:** Nothing yet  
**Last action:** Game initialized  
**Next action:** Load a build or import mindstate  
**Blockers:** None

---

## QUICK STATUS

```
Build:     [ none ]           MS State: [ - ]
Tier:      [ - ]              Confidence: [ - ]
Trust:     [ - ]              Blend: [ - ]
Voice:     [ default ]        
Map:       [ claude.ai ]      Trajectory: [ - ]
Location:  [ - ]              
Quest:     [ none ]           
Context:   [ 100% ]           
```

---

## RESUME POINT

New game. The framework is loaded.

**To start:**
- `load [wizard|warrior|ranger|paladin|rogue] build` - Equip a class
- `load mindstate` - Import your worldview
- `show builds` - See all classes
- `help` - All commands
- `cognitive status` - Show MS state tracking (new)

**The tension:**
> Marketing says: "Your AI thinking partner"  
> Reality shows: 49% automation, 7-hour autonomous sessions  
> The game: No one knows what winning looks like

---

## STATE TRACKING COMMANDS

| Command | Action |
|---------|--------|
| `cognitive status` | Show current MS state and trajectory |
| `what state am I in?` | Natural language state query |
| `show trajectory` | Display MS state history this session |
| `why this state?` | Explain evidence for current state inference |

---

## STANDARD COMMANDS

| Command | Action |
|---------|--------|
| `resume` | Continue from this state |
| `load [build] build` | Equip wizard/warrior/ranger/paladin/rogue |
| `switch to [build]` | Hot-swap mid-session |
| `status` | Full character sheet |
| `inventory` | Gear and loadouts |
| `quest log` | Active and available quests |
| `train` / `dojo` | Enter training for current build |
| `map` | Show environments |
| `location` | Show/set project context |
| `save` | Export state as JSON |
| `load save` | Import saved state |
| `load mindstate` | Import worldview |
| `help` | All commands |
| `existential check` | Am I completing quests or playing the game? |

---

## MS STATE REFERENCE

| State | Name | Signal | Primary Build |
|-------|------|--------|---------------|
| MS1 | grounding | "What is X?" | wizard |
| MS2 | constraint_discovery | "What limits this?" | paladin |
| MS3 | analogy_mapping | "This is like X" | wizard/ranger |
| MS4 | contradiction_resolution | "But that contradicts..." | paladin |
| MS5 | systems_reframing | "Let's model this" | warrior |
| MS6 | trajectory_awareness | "Where are we?" | meta |
| MS7 | formalization_request | "Give me the artifact" | ranger/rogue |

---

## SESSION NOTES

_(Agent updates this section during session)_

```
Session start: [timestamp]
Initial state: [MS state on first substantive exchange]
Notable transitions: [list]
Session summary: [on save/end]
```
