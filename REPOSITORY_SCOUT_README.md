# Repository Scout

A CLI tool for discovering and managing git repositories on your system.

## Features

- **Scan**: Find all git repos in a directory (configurable depth)
- **List**: Display discovered repos with branch and remote info
- **Create**: Initialize new git repos from the command line
- **Info**: Show detailed repository information
- **Status**: Display git status for any repo
- **Cache**: Fast lookups with automatic caching

## Usage

```bash
./repo-scout.sh scan [path] [depth]    # Scan for repos (default: current dir, depth 3)
./repo-scout.sh list                   # List all cached repos
./repo-scout.sh create [path] [name]   # Create new repo
./repo-scout.sh info [repo]            # Show repo details
./repo-scout.sh status [repo]          # Show git status
./repo-scout.sh cache-clear            # Clear the cache
./repo-scout.sh help                   # Show help
```

## Examples

```bash
# Scan home directory for repos
./repo-scout.sh scan ~

# List all discovered repos
./repo-scout.sh list

# Create a new project
./repo-scout.sh create ~/my-project MyApp

# Check repo status
./repo-scout.sh status ~/my-project
```

## Quest Info

**Quest**: The Repository Scout  
**Build**: Rogue (CLI Master)  
**Tier**: Pickpocket  
**Status**: Complete ✅

**Skills Unlocked**:
- Shadow Walking (filesystem navigation)
- Sleight of Hand (file manipulation)

**Branch**: feat/repository-scout  
**Commits**: 3
