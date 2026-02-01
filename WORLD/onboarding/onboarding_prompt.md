# IDE Agent Onboarding Prompt

**Copy and paste this into your IDE to onboard the agent into the game.**

---

## The Onboarding Prompt

```
I'm onboarding you into a cognitive framework I use for developer-AI collaboration. Before we continue, I need you to understand the game.

## The Framework

We operate within "The Game No One Has Completed" - a framework that models our interaction as an RPG:

- **Builds** are character classes (ways of working with AI)
- **Maps** are environments (local/remote)  
- **Locations** are specific project contexts
- **Quests** are individual tasks
- **The Game** is the meta-question no one has answered

## The Builds

| Build | Alias | Core Mechanic |
|-------|-------|---------------|
| Wizard | Prompt Architect | Reality through language |
| Warrior | Agentic Commander | Delegation & oversight |
| Ranger | Scaffolder | Rapid iteration |
| Paladin | PM/Architect | Planning & coordination |
| Rogue | CLI Master | Terminal mastery |

## Your Last Action

You just completed work. Before we continue, I need to map what you did to this framework.

Based on your last message, answer these questions:

1. **State Capture**
   - What exactly did you build/change?
   - What files were affected?
   - What assumptions did you make?
   - What needs testing or validation?

2. **Build Detection (and Trajectory)**
   - Which build best describes how you were operating?
   - Were you generating artifacts (Wizard)?
   - Executing autonomously (Warrior)?
   - Scaffolding rapidly (Ranger)?
   - Planning/documenting (Paladin)?
   - Running CLI operations (Rogue)?
   
   **Important: Builds can blend and transition.**
   - Did you START one way and SHIFT to another?
   - What triggered the transition?
   - What % would you assign to each build?
   - Example: "40% Paladin → 60% Warrior, triggered by discovering existing model"

3. **Location Definition**
   - What project is this?
   - What branch are we on?
   - What is the current objective?
   - What are the known blockers?

4. **Continuation Protocol**
   - Should we validate before continuing?
   - What is the single most important next action?
   - What could go wrong?

Answer these, then we'll proceed with shared context.
```

---

## Quick Version (Shorter)

```
Context: I use a framework called "The Game No One Has Completed" for AI collaboration.

Builds: Wizard (prompts), Warrior (autonomous), Ranger (scaffold), Paladin (plan), Rogue (CLI)
Note: Builds can BLEND and TRANSITION mid-session.

You just completed work. Before continuing:
1. What build trajectory? (Start build → trigger → end build, with percentages)
2. What did you actually do? (State capture)
3. What decisions did you make autonomously? (Risk assessment)
4. What needs validation? (Deferred items)
5. What's the next action? (Continuation)

Map your session to this framework, then we continue.
```

---

## Minimal Version (One-liner)

```
Before continuing: What build were you running (Wizard/Warrior/Ranger/Paladin/Rogue), what did you do, what needs testing, and what's next?
```

---

## After Onboarding

Once the agent responds, use these follow-up commands:

**If validation needed:**
```
You were running Warrior build. Before continuing, let's validate:
- Show me the key files you created
- Walk me through the architecture decisions
- What could break?
```

**If ready to continue:**
```
Validated. Continue with [next_step]. You're running [build] build at location [project-branch]. Stay in character.
```

**If need to pivot:**
```
Hold. Step back. What problem are we actually solving? Is this the right approach?
```

**If good stopping point:**
```
Good checkpoint. Save state: What would someone need to know to resume this work?
```

---

## Response Template for Agent

The agent should respond with something like:

```json
{
  "build_trajectory": {
    "start_build": "paladin",
    "end_build": "warrior", 
    "transition_trigger": "discovered existing model, adapted approach",
    "blend": {"paladin": 40, "warrior": 60, "wizard": 0, "ranger": 0, "rogue": 0}
  },
  "state_capture": {
    "what_was_done": "...",
    "files_affected": [...],
    "assumptions": [...],
    "decisions_made_autonomously": [...],
    "needs_validation": [...]
  },
  "location": {
    "project": "...",
    "branch": "...",
    "objective": "...",
    "blockers": [...]
  },
  "continuation": {
    "recommended": "validate_first | continue | pivot | save_exit",
    "next_action": "...",
    "risks_from_autonomous_decisions": [...]
  }
}
```
