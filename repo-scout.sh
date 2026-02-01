#!/bin/bash

# Repository Scout - Find and manage git repos on your PC
# Rogue Tier 1: Pickpocket - Shadow Walking & Sleight of Hand

set -e

SCOUT_HOME="${SCOUT_HOME:-.}"
REPOS_CACHE="$SCOUT_HOME/.repos_cache"

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

show_help() {
  cat << 'EOF'
Repository Scout - Discover and manage git repos

USAGE:
  repo-scout [command] [options]

COMMANDS:
  scan [path]           Scan directory for git repos (default: ~)
  list                  List all discovered repos
  create [path] [name]  Create new git repo
  info [repo]           Show repo details
  status [repo]         Show repo status (staged, commits, branch)
  cache-clear           Clear the repos cache
  help                  Show this help

EXAMPLES:
  repo-scout scan ~                    # Scan home directory
  repo-scout scan ~/projects           # Scan specific directory
  repo-scout list                      # List all cached repos
  repo-scout create ~/my-project MyApp # Create new repo
  repo-scout info ~/my-project         # Show repo info
  repo-scout status ~/my-project       # Show git status

EOF
}

# ============================================================================
# SCANNING & DISCOVERY
# ============================================================================

scan_for_repos() {
  local search_path="${1:-.}"
  local max_depth="${2:-3}"
  
  echo -e "${BLUE}🔍 Scanning for git repos in: $search_path${NC}"
  
  local repos=()
  
  # Find all .git directories, limit depth to avoid deep recursion
  while IFS= read -r git_dir; do
    local repo_path=$(dirname "$git_dir")
    repos+=("$repo_path")
  done < <(find "$search_path" -maxdepth "$max_depth" -type d -name ".git" 2>/dev/null)
  
  if [ ${#repos[@]} -eq 0 ]; then
    echo -e "${YELLOW}⚠️  No git repos found${NC}"
    return 1
  fi
  
  # Save to cache
  mkdir -p "$(dirname "$REPOS_CACHE")"
  printf '%s\n' "${repos[@]}" > "$REPOS_CACHE"
  
  echo -e "${GREEN}✓ Found ${#repos[@]} repo(s)${NC}"
  return 0
}

list_repos() {
  if [ ! -f "$REPOS_CACHE" ]; then
    echo -e "${YELLOW}No cached repos. Run 'scan' first.${NC}"
    return 1
  fi
  
  echo -e "${BLUE}📦 Discovered Repositories:${NC}"
  echo ""
  
  local count=0
  while IFS= read -r repo; do
    count=$((count + 1))
    local branch=$(cd "$repo" && git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    local remote=$(cd "$repo" && git config --get remote.origin.url 2>/dev/null || echo "no remote")
    
    printf "  ${GREEN}%d.${NC} %s\n" "$count" "$repo"
    printf "     Branch: %s | Remote: %s\n" "$branch" "$remote"
  done < "$REPOS_CACHE"
  
  echo ""
}

# ============================================================================
# REPO CREATION
# ============================================================================

create_repo() {
  local repo_path="$1"
  local repo_name="${2:-$(basename "$repo_path")}"
  
  if [ -z "$repo_path" ]; then
    echo -e "${RED}✗ Error: Path required${NC}"
    return 1
  fi
  
  if [ -d "$repo_path/.git" ]; then
    echo -e "${YELLOW}⚠️  Repo already exists at $repo_path${NC}"
    return 1
  fi
  
  echo -e "${BLUE}⚔️  Creating new repo: $repo_name${NC}"
  
  mkdir -p "$repo_path"
  cd "$repo_path"
  
  git init
  git config user.name "Repository Scout"
  git config user.email "scout@local"
  
  # Create initial files
  echo "# $repo_name" > README.md
  echo "node_modules/" > .gitignore
  echo ".DS_Store" >> .gitignore
  
  git add .
  git commit -m "Initial commit by Repository Scout"
  
  echo -e "${GREEN}✓ Repo created at $repo_path${NC}"
  
  # Add to cache
  echo "$repo_path" >> "$REPOS_CACHE"
}

# ============================================================================
# REPO INFO & STATUS
# ============================================================================

show_repo_info() {
  local repo_path="$1"
  
  if [ ! -d "$repo_path/.git" ]; then
    echo -e "${RED}✗ Not a git repo: $repo_path${NC}"
    return 1
  fi
  
  cd "$repo_path"
  
  echo -e "${BLUE}📋 Repository Info:${NC}"
  echo ""
  printf "  Path:     %s\n" "$repo_path"
  printf "  Branch:   %s\n" "$(git rev-parse --abbrev-ref HEAD)"
  printf "  Remote:   %s\n" "$(git config --get remote.origin.url || echo 'none')"
  printf "  Commits:  %s\n" "$(git rev-list --count HEAD)"
  printf "  Last:     %s\n" "$(git log -1 --format='%ar' 2>/dev/null || echo 'N/A')"
  echo ""
}

show_repo_status() {
  local repo_path="$1"
  
  if [ ! -d "$repo_path/.git" ]; then
    echo -e "${RED}✗ Not a git repo: $repo_path${NC}"
    return 1
  fi
  
  cd "$repo_path"
  
  echo -e "${BLUE}🔄 Repository Status:${NC}"
  echo ""
  git status --short
  echo ""
}

# ============================================================================
# CACHE MANAGEMENT
# ============================================================================

clear_cache() {
  if [ -f "$REPOS_CACHE" ]; then
    rm "$REPOS_CACHE"
    echo -e "${GREEN}✓ Cache cleared${NC}"
  else
    echo -e "${YELLOW}No cache to clear${NC}"
  fi
}

# ============================================================================
# MAIN
# ============================================================================

main() {
  local cmd="${1:-help}"
  
  case "$cmd" in
    scan)
      scan_for_repos "${2:-.}" "${3:-3}"
      ;;
    list)
      list_repos
      ;;
    create)
      create_repo "$2" "$3"
      ;;
    info)
      show_repo_info "$2"
      ;;
    status)
      show_repo_status "$2"
      ;;
    cache-clear)
      clear_cache
      ;;
    help|--help|-h)
      show_help
      ;;
    *)
      echo -e "${RED}Unknown command: $cmd${NC}"
      show_help
      exit 1
      ;;
  esac
}

main "$@"
