# Claude Game Saves

**The Game No One Has Completed**

A cognitive framework for understanding and navigating developer interactions with Claude and AI-assisted development.

## Philosophy

This framework treats the developer-AI relationship as an RPG:
- **Builds** are character classes (ways of using Claude)
- **Maps** are environments (local/remote)
- **Locations** are specific project contexts
- **Quests** are individual tasks
- **The Game** is the meta-question no one has answered yet

## Quick Start

1. Choose a build that matches your playstyle
2. Load the MCP config for your build
3. Select a map and location
4. Start playing

## Directory Structure

```
claude-game-saves/
├── builds/              # Character classes
│   ├── wizard/          # Prompt Architect
│   ├── warrior/         # Agentic Commander
│   ├── ranger/          # Scaffolder
│   ├── paladin/         # PM/Architect
│   └── rogue/           # CLI Master
├── maps/                # Environments
│   ├── local/           # Your machine
│   └── remote/          # Cloud/servers
├── locations/           # Specific contexts
├── mindstates/          # Philosophical frameworks
├── quick_loads/         # Context loading commands
└── onboarding/          # IDE agent onboarding protocols
```

## Onboarding an IDE Agent

When an AI IDE has done work without game context:

```
You just completed work. Before continuing: 
What build were you running (Wizard/Warrior/Ranger/Paladin/Rogue), 
what did you do, what needs testing, and what's next?
```

For autonomous work that needs review:
```
You were running WARRIOR build - autonomous execution. 
Walk me through what you built and let's validate before continuing.
```

See `onboarding/` for full protocols and examples.

## Builds

| Build | Alias | Core Mechanic | Best For |
|-------|-------|---------------|----------|
| Wizard | Prompt Architect | Reality through language | Creative generation |
| Warrior | Agentic Commander | Delegation & oversight | Autonomous coding |
| Ranger | Scaffolder | Rapid iteration | Prototyping |
| Paladin | PM/Architect | Planning & coordination | System design |
| Rogue | CLI Master | Terminal mastery | DevOps, automation |

## Quick Load Commands

### Load a Build
```
Load wizard build. Ready to cast.
Load warrior build. Ready to command.
Load ranger build. Ready to scaffold.
Load paladin build. Ready to plan.
Load rogue build. Ready to strike.
```

### Resume Session
```
I'm loading my save file. Remind me: what build am I running?
```

### Existential Check
```
Am I completing quests or playing the game?
```

## The Tension

> Marketing says: "Your AI thinking partner"
> 
> Reality shows: 49% automation, 7-hour autonomous sessions
> 
> The game: No one knows what winning looks like

## License

Public domain. Copy, modify, extend. The game belongs to everyone playing it.
