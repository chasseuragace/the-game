# Multi-Agent Orchestration

**The Runtime We Designed, Now Implemented**

---

## What This Is

The `your-claude-engineer` harness is a **production implementation** of multi-agent orchestration. It maps directly to our framework:

| Game Concept | Harness Implementation |
|--------------|------------------------|
| Warrior build (Commander trust) | Orchestrator agent |
| Paladin aspects | Linear agent (task management) |
| Warrior aspects | Coding agent (implementation) |
| Rogue aspects | GitHub agent (git ops) |
| Session handoff | META issue + .linear_project.json |
| RESUME.md | Progress tracker + session comments |
| Gear/MCP loadouts | Arcade MCP gateway |
| Context management | Sub-agent isolation |

---

## The Core Insight

> "Agents don't do that well when you start to fill their context window. It is the most precious resource."

The harness solves this by:
1. **Sub-agent isolation** — each agent gets fresh context
2. **Session handoff** — state persists between sessions
3. **Orchestrator coordination** — passes context explicitly, never assumes shared memory

This IS the runtime_rules.md Section 6.3 (Agent ↔ Agent) — implemented.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (Haiku)                         │
│                    "The Game Engine"                            │
│                                                                 │
│  Reads: .linear_project.json, META issue                        │
│  Decides: What to work on next                                  │
│  Delegates: To specialized agents                               │
│  Maintains: Session continuity                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
  ┌────▼─────┐    ┌─────▼──────┐   ┌─────▼──────┐
  │  LINEAR  │    │   CODING   │   │   GITHUB   │
  │  Agent   │    │   Agent    │   │   Agent    │
  │ (Haiku)  │    │  (Sonnet)  │   │  (Haiku)   │
  │          │    │            │   │            │
  │ Paladin  │    │  Warrior   │   │   Rogue    │
  │ aspects  │    │  aspects   │   │  aspects   │
  └────┬─────┘    └─────┬──────┘   └─────┬──────┘
       │                │                 │
  ┌────▼─────┐          │                 │
  │  SLACK   │          │                 │
  │  Agent   │          │                 │
  │ (Haiku)  │          │                 │
  └──────────┘          │                 │
                        │                 │
       ┌────────────────▼─────────────────▼───────┐
       │         PROJECT OUTPUT                   │
       │    (Isolated Git Repository)             │
       └──────────────────────────────────────────┘
```

---

## Session Flow

### First Run (Initialization)

```
1. Orchestrator reads app_spec.txt (PRD)
2. Delegates to Linear agent:
   - Create project
   - Create issues (features)
   - Create META issue (progress tracker)
3. Delegates to GitHub agent:
   - Init repository
   - Create README, init.sh, .gitignore
   - Push to remote if configured
4. Creates .linear_project.json (local pointer)
5. Optionally: Start first feature
```

### Continuation Loop

```
1. ORIENT
   - Read .linear_project.json (project ID)
   - Ask Linear agent for status
   
2. VERIFY (Mandatory Gate)
   - Ask Coding agent to test existing features
   - If FAIL → Fix regression first
   - If PASS → Continue
   
3. IMPLEMENT
   - Get full issue context from Linear
   - Pass COMPLETE context to Coding agent
   - Coding agent implements + tests via Playwright
   - Screenshot evidence required
   
4. COMMIT
   - Ask GitHub agent to commit + push
   - Pass files changed, issue ID
   
5. UPDATE
   - Ask Linear agent to mark Done
   - Pass screenshot evidence paths
   
6. HANDOFF
   - Update META issue with session summary
   - Loop or end
```

---

## Critical Protocol: Context Passing

> "Agents don't share memory. YOU must pass information between them."

**Anti-pattern:**
```
❌ "Ask coding agent to check Linear for the next issue"
```

**Correct:**
```
✅ Linear agent returns: { issue_id, title, description, test_steps }
   ↓
   Orchestrator passes full context to coding agent:
   "Implement issue ABC-123: [full context]"
   ↓
   Coding agent returns: { files_changed, screenshot_evidence }
   ↓
   Orchestrator passes to Linear agent:
   "Mark ABC-123 done with evidence: [paths]"
```

This maps to runtime_rules.md Section 6.1 — explicit state transfer.

---

## Mapping to Builds

The harness implements **build blending** at the infrastructure level:

### Orchestrator = Game Engine
- Coordinates all builds
- Maintains session state
- Decides what to work on

### Linear Agent = Paladin Mode
- Task management
- Status tracking
- Documentation (META comments)
- "What needs to be designed before built?"

### Coding Agent = Warrior Mode
- Autonomous execution
- Implementation
- Testing (Playwright)
- "Mission objective received. Deploying."

### GitHub Agent = Rogue Mode
- Git operations
- Commits, branches, PRs
- "Precision strike on the repository."

### Slack Agent = Communication
- Progress updates
- Milestone notifications
- Human-in-loop touchpoints

---

## Trust Level: Commander

This harness operates at **Warrior Trust Level 4: Commander**

| Aspect | Implementation |
|--------|----------------|
| Autonomy | Project scope |
| Review | Strategic (PR at session end) |
| Duration | Multi-hour/multi-session |
| Human touchpoint | Slack notifications |
| Rollback | Git history |

The verification gate is corrigibility infrastructure:
- Test before new work
- Screenshot evidence required
- No Done without proof

---

## Arcade MCP Gateway

Single authentication for 91 tools:
- Linear (39 tools)
- GitHub (46 tools)
- Slack (8 tools)

Uses **tool discovery** — not dumping all definitions into context.

This IS the INVENTORY/armory.json concept at scale.

---

## Integration with Game Framework

### As a Build Configuration

The harness can be loaded as a **Warrior Commander loadout**:

```json
{
  "build": "warrior",
  "trust_level": "commander",
  "gear": {
    "orchestration": "your-claude-engineer",
    "task_management": "linear",
    "version_control": "github",
    "communication": "slack"
  },
  "sub_agents": ["linear", "coding", "github", "slack"]
}
```

### As a Location

A project using the harness is a **Location**:

```json
{
  "id": "pomodoro-timer-harness",
  "map_type": "local",
  "map_subtype": "harness",
  "project": {
    "name": "pomodoro-timer",
    "path": "./generations/pomodoro-timer",
    "linear_project_id": "...",
    "github_repo": "owner/pomodoro-timer"
  },
  "state": {
    "issues_total": 5,
    "issues_done": 5,
    "current_session": "complete"
  }
}
```

### As a Quest

"Build X autonomously" becomes a quest type:

```json
{
  "quest": "autonomous_build",
  "name": "The Long Build",
  "description": "Let the harness build an application autonomously",
  "input": "app_spec.txt",
  "output": "Working application + Linear project + GitHub repo",
  "trust_required": "commander",
  "human_checkpoints": ["slack_notifications", "pr_review"]
}
```

---

## The Tension (Realized)

> Marketing says: "Your AI thinking partner"
> Reality shows: 49% automation, 7-hour autonomous sessions
> The game: No one knows what winning looks like

This harness IS the 7-hour autonomous session. It's real. It works.

The framework gives us the language to talk about it:
- What build am I running? (Warrior Commander)
- What trust level? (Autonomous/Commander)
- What's my checkpoint? (Slack notification, PR review)
- How do I resume? (META issue, .linear_project.json)

---

## Files Reference

The harness lives in `WORLD/orchestration/`:

```
orchestration/
├── ORCHESTRATION.md          ← This file
├── prompts/
│   ├── orchestrator.md       ← Main coordinator prompt
│   ├── coding_agent.md       ← Implementation prompt
│   ├── linear_agent.md       ← Task management prompt
│   ├── github_agent.md       ← Git operations prompt
│   └── slack_agent.md        ← Communication prompt
├── agents/
│   └── definitions.json      ← Agent configurations
└── security/
    └── allowed_commands.json ← Bash allowlist
```

---

## Usage

### From Claude.ai (Manual)

```
Load warrior build at commander trust.
I want to use the orchestration harness.
Here's my app spec: [paste PRD]
```

### From CLI (Automated)

```bash
# Set up environment
source venv/bin/activate

# Run harness
python autonomous_agent_demo.py --project-dir my-app
```

### Hybrid

```
1. Design with Paladin (PRD → app_spec.txt)
2. Deploy with Warrior Commander (harness)
3. Review with human (Slack + PR)
4. Iterate with Wizard (conversation refinement)
```

---

## The Meta-Insight

The harness answers a question from our SRS:

> "What does it mean to be a developer when AI codes autonomously?"

**Answer:** You become the architect who:
1. Writes the spec (Paladin)
2. Configures the trust level (Warrior)
3. Reviews the output (Human)
4. Iterates the conversation (Wizard)

The builds aren't just playstyles — they're phases of a workflow.

---

*"The harness is the game made real. The game is the harness made playable."*
