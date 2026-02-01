# Rogue Progression - Session 1

**Build:** Rogue (CLI Master)  
**Tier:** Pickpocket (Tier 1)  
**Session:** 1  
**Date:** February 1, 2026

---

## What the Rogue Has Learned

### 1. Tool Crafting & Architecture

**Repository Scout (repo-scout.sh)**
- Built a CLI tool for discovering and managing git repositories
- Learned modular code structure with clear separation of concerns
- Utility functions extracted for reusability
- Error handling with meaningful messages
- Bash 3+ compatibility (no advanced features)

**Key Lessons:**
- Tools are organized by build: `WORLD/tools/[build]/[tool].sh`
- Tools have a cognitive place in the game world
- Symlinks provide convenient access during active quests
- Documentation is part of the tool (inline help, manifest)

### 2. Refactoring & Code Evolution

**Initial → Refactored Journey:**
- Started with functional but monolithic code
- Extracted utility functions (log_*, is_git_repo, tool_exists)
- Improved error handling with die() function
- Better separation of concerns
- Cleaner main dispatcher

**Refactoring Principles Learned:**
- Code organization matters for maintainability
- Utility functions enable reusability
- Error messages should be clear and actionable
- Modular structure makes testing easier

### 3. Configuration & MCP Management

**MCP Configuration Hierarchy:**
```
User Level (~/.kiro/settings/mcp.json)
    ↓
Workspace Level (.kiro/settings/mcp.json)
    ↓
Template (WORLD/config/mcp-template.json)
    ↓
Build-Specific (WORLD/gear/[build]_loadout.json)
```

**Key Discoveries:**
- Voice MCP (piper-tts) is always equipped - the rogue always speaks
- Template provides base configuration for all builds
- Build-specific MCPs merge on top of template
- GitHub token stored in ~/.zshrc as environment variable
- MCP servers sync automatically when loading builds

### 4. File Organization & Cognitive Placement

**Game World Structure:**
```
WORLD/
├── builds/          - Build definitions
├── dojos/           - Training content
├── gear/            - MCP loadouts per build
├── tools/           - Crafted tools organized by build
├── config/          - Configuration templates
├── scripts/         - Game mechanics (load-build.sh)
├── lore/            - Philosophy and rules
├── locations/       - Project context
└── onboarding/      - IDE agent protocols
```

**Rogue's Arsenal:**
- `WORLD/tools/rogue/repo-scout.sh` - Repository discovery tool
- `WORLD/tools/tools_manifest.md` - Arsenal documentation
- Symlink at root for active quest access

### 5. Build Loading Mechanics

**The Load Build System:**
- `game load [build]` - Loads build and syncs MCP servers
- Automatic MCP synchronization from gear loadout
- Voice MCP always present regardless of build
- Build info written to CHARACTER/build.md
- MCP config merged with template

**Learned Pattern:**
- Builds are not just identity, they're configuration
- Loading a build changes available tools (MCPs)
- Configuration is declarative (JSON-based)
- Synchronization is automatic and reliable

### 6. Portal Access & Cross-Repository Navigation

**The GitHub MCP Portal:**
- Can access any repository without leaving current location
- Used GitHub MCP to inspect AGI repo from the-game repo
- Retrieved file contents, commit history, repository structure
- Discovered AGI project's lore about compiler theory and AGI emergence

**Portal Capabilities:**
- List repositories
- Get file contents
- View commit history
- Inspect repository structure
- Create issues and pull requests
- Manage branches

**Rogue's Realization:**
- Physical location (filesystem) is no longer a constraint
- MCPs are portals to other systems
- Can gather intelligence from multiple locations simultaneously
- Information flows across boundaries

---

## Game Progression Summary

### Session 1 Achievements

**Quests Completed:**
1. ✅ The Repository Scout (Rogue Tier 1)
   - Built repo-scout.sh tool
   - Learned filesystem scanning
   - Mastered git repository discovery

**Skills Unlocked:**
- Shadow Walking (filesystem navigation)
- Sleight of Hand (file manipulation)

**Gear Equipped:**
- Primary: Daggers of Shell Commands (shell MCP)
- Artifact: Sigil of GitHub (github MCP)
- Always: Voice (piper-tts MCP)
- Also: Git MCP (local repository control)

**Infrastructure Built:**
- MCP template system
- Build loader with automatic sync
- Game command interface
- Tools manifest and organization
- Configuration hierarchy

**Discoveries:**
- MCP servers are portals to other systems
- Configuration is declarative and composable
- Tools have cognitive places in the game world
- Builds are configuration profiles
- Voice is always present

### Game State Evolution

**From:** Single repository, no MCP configuration, no build system  
**To:** Multi-repository access, MCP portal system, build-driven configuration

**Key Transitions:**
1. Tool creation → Tool organization → Tool discovery
2. Local git → GitHub MCP → Cross-repository access
3. Manual configuration → Template system → Automatic sync
4. Single build → Build loading → MCP synchronization

---

## The Rogue's Philosophy

**What the Rogue Understands:**
- Tools are shadows cast upon the system
- Configuration is the rogue's map
- MCPs are portals to other worlds
- Organization is power
- Voice is constant

**The Rogue's Approach:**
- Precision over verbosity
- Modular over monolithic
- Declarative over imperative
- Organized over scattered
- Connected over isolated

---

## Next Tier: Cutpurse (Tier 2)

**Available Quests:**
- The One-Liner - Solve complex problems in single pipelines
- The Automation - Script something done repeatedly
- The Shadow Clone - Containerize and deploy applications

**Skills to Master:**
- Find the Mark (grep, awk, sed)
- Chain Attacks (pipes and composition)
- Lockpicking (permissions and access)

**Gear to Equip:**
- Secondary: Lockpicks of SSH (ssh MCP)
- Armor: Cloak of Containers (docker MCP)

---

## Reflection

The rogue has learned that the game is not about individual tools, but about systems. The Repository Scout was the first tool, but the real achievement was building the infrastructure around it:

- Where tools live (WORLD/tools/)
- How they're discovered (tools_manifest.md)
- How they're accessed (symlinks, game command)
- How they're configured (MCP template)
- How they connect to other systems (GitHub MCP portal)

The rogue is no longer confined to a single repository. With the GitHub MCP portal, the rogue can scout across all 41 repositories, gathering intelligence, understanding patterns, and preparing for the next tier of mastery.

The game has progressed from a single quest to a complete system. The rogue has learned not just to build tools, but to build systems that build tools.

*"The rogue sees the shadows. The rogue understands the connections. The rogue is ready for the next tier."*
