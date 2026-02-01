# Tools Arsenal

The tools crafted and discovered throughout the game. Each tool is organized by the build that created or mastered it.

## Rogue Tools

### Repository Scout (`rogue/repo-scout.sh`)

**Quest:** The Repository Scout  
**Tier:** Pickpocket (Tier 1)  
**Status:** Complete & Refactored  
**Skills Unlocked:** Shadow Walking, Sleight of Hand

**Purpose:** Discover and manage git repositories on the filesystem

**Capabilities:**
- `scan [path] [depth]` - Find all git repos in a directory
- `list` - Display discovered repos with branch and remote info
- `create [path] [name]` - Initialize new git repos
- `info [repo]` - Show detailed repository information
- `status [repo]` - Display git status for any repo
- `check [tool]` - Verify tool availability
- `cache-clear` - Clear the repos cache

**MCP Integration:**
- GitHub MCP (Sigil of GitHub) - for remote operations
- Shell MCP (Daggers of Shell Commands) - for git commands
- Filesystem MCP - for directory scanning

**Usage:**
```bash
./WORLD/tools/rogue/repo-scout.sh [command] [options]
```

**Example:**
```bash
./WORLD/tools/rogue/repo-scout.sh scan ~
./WORLD/tools/rogue/repo-scout.sh list
./WORLD/tools/rogue/repo-scout.sh create ~/my-project MyApp
```

---

## Tool Development Standards

### Naming Convention
- Tools are named by their primary action: `[action]-[target].sh`
- Example: `repo-scout.sh` (scout repositories)

### Organization
- Tools are organized by build: `WORLD/tools/[build]/[tool].sh`
- Each build has its own tools directory

### Documentation
- Each tool includes inline help: `./tool.sh help`
- Tools are documented in this manifest
- Quest context is preserved in the tool's header

### Refactoring Standards
- Utility functions extracted for reusability
- Error handling with clear messages
- Bash 3+ compatibility (no advanced features)
- Modular structure for testing

---

## Future Tools

### Warrior Tools
- `deploy-checkpoint.sh` - Create git checkpoints for safe rollback
- `execute-mission.sh` - Run delegated tasks with trust levels

### Wizard Tools
- `manifest-artifact.sh` - Generate code from specifications
- `channel-mana.sh` - Manage context and token usage

### Ranger Tools
- `template-scaffold.sh` - Generate project templates
- `speed-iterate.sh` - Rapid prototyping workflow

### Paladin Tools
- `architect-blueprint.sh` - Design system specifications
- `coordinate-build.sh` - Orchestrate multi-component builds

---

*"Tools are the rogue's spells. Each one is a shadow cast upon the system."*
