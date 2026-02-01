#!/bin/bash

# Repository Scout - Find and manage git repos on your PC
# Rogue Tier 1: Pickpocket - Shadow Walking & Sleight of Hand
# Refactored for clarity and maintainability

set -euo pipefail

# ============================================================================
# CONFIGURATION
# ============================================================================

readonly SCOUT_HOME="${SCOUT_HOME:-.}"
readonly REPOS_CACHE="$SCOUT_HOME/.repos_cache"
readonly SCRIPT_NAME="$(basename "$0")"

# Color codes
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly BLUE='\033[0;34m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

log_error() {
  echo -e "${RED}✗ $*${NC}" >&2
}

log_success() {
  echo -e "${GREEN}✓ $*${NC}"
}

log_info() {
  echo -e "${BLUE}$*${NC}"
}

log_warn() {
  echo -e "${YELLOW}⚠️  $*${NC}"
}

die() {
  log_error "$@"
  exit 1
}

is_git_repo() {
  [ -d "$1/.git" ]
}

tool_exists() {
  command -v "$1" &> /dev/null
}

# ============================================================================
# CACHE OPERATIONS
# ============================================================================

ensure_cache_dir() {
  mkdir -p "$(dirname "$REPOS_CACHE")"
}

save_repos_to_cache() {
  local repos_str="$1"
  ensure_cache_dir
  echo "$repos_str" > "$REPOS_CACHE"
}

load_repos_from_cache() {
  if [ ! -f "$REPOS_CACHE" ]; then
    return 1
  fi
  cat "$REPOS_CACHE"
}

clear_cache() {
  if [ -f "$REPOS_CACHE" ]; then
    rm "$REPOS_CACHE"
    log_success "Cache cleared"
  else
    log_warn "No cache to clear"
  fi
}

# ============================================================================
# SCANNING & DISCOVERY
# ============================================================================

scan_for_repos() {
  local search_path="${1:-.}"
  local max_depth="${2:-3}"
  
  log_info "🔍 Scanning for git repos in: $search_path"
  
  local repos_str=""
  
  while IFS= read -r git_dir; do
    repos_str="$repos_str$(dirname "$git_dir")"$'\n'
  done < <(find "$search_path" -maxdepth "$max_depth" -type d -name ".git" 2>/dev/null)
  
  if [ -z "$repos_str" ]; then
    log_warn "No git repos found"
    return 1
  fi
  
  save_repos_to_cache "$repos_str"
  local count
  count=$(echo "$repos_str" | grep -c . || true)
  log_success "Found $count repo(s)"
}

# ============================================================================
# REPO LISTING
# ============================================================================

list_repos() {
  local repos
  if ! repos=$(load_repos_from_cache); then
    log_warn "No cached repos. Run 'scan' first."
    return 1
  fi
  
  log_info "📦 Discovered Repositories:"
  echo ""
  
  local count=0
  while IFS= read -r repo; do
    [ -z "$repo" ] && continue
    count=$((count + 1))
    
    local branch remote
    branch=$(cd "$repo" && git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    remote=$(cd "$repo" && git config --get remote.origin.url 2>/dev/null || echo "no remote")
    
    printf "  ${GREEN}%d.${NC} %s\n" "$count" "$repo"
    printf "     Branch: %s | Remote: %s\n" "$branch" "$remote"
  done <<< "$repos"
  
  echo ""
}

# ============================================================================
# REPO CREATION
# ============================================================================

create_repo() {
  local repo_path="$1"
  local repo_name="${2:-$(basename "$repo_path")}"
  
  [ -z "$repo_path" ] && die "Path required"
  is_git_repo "$repo_path" && die "Repo already exists at $repo_path"
  
  log_info "⚔️  Creating new repo: $repo_name"
  
  mkdir -p "$repo_path"
  cd "$repo_path"
  
  git init
  git config user.name "Repository Scout"
  git config user.email "scout@local"
  
  echo "# $repo_name" > README.md
  {
    echo "node_modules/"
    echo ".DS_Store"
  } > .gitignore
  
  git add .
  git commit -m "Initial commit by Repository Scout"
  
  log_success "Repo created at $repo_path"
  
  ensure_cache_dir
  echo "$repo_path" >> "$REPOS_CACHE"
}

# ============================================================================
# REPO INFORMATION
# ============================================================================

show_repo_info() {
  local repo_path="$1"
  
  [ -z "$repo_path" ] && die "Path required"
  is_git_repo "$repo_path" || die "Not a git repo: $repo_path"
  
  cd "$repo_path"
  
  local branch commits last_commit remote
  branch=$(git rev-parse --abbrev-ref HEAD)
  commits=$(git rev-list --count HEAD)
  last_commit=$(git log -1 --format='%ar' 2>/dev/null || echo "N/A")
  remote=$(git config --get remote.origin.url || echo "none")
  
  log_info "📋 Repository Info:"
  echo ""
  printf "  Path:     %s\n" "$repo_path"
  printf "  Branch:   %s\n" "$branch"
  printf "  Remote:   %s\n" "$remote"
  printf "  Commits:  %s\n" "$commits"
  printf "  Last:     %s\n" "$last_commit"
  echo ""
}

show_repo_status() {
  local repo_path="$1"
  
  [ -z "$repo_path" ] && die "Path required"
  is_git_repo "$repo_path" || die "Not a git repo: $repo_path"
  
  cd "$repo_path"
  
  log_info "🔄 Repository Status:"
  echo ""
  git status --short
  echo ""
}

# ============================================================================
# HELP & USAGE
# ============================================================================

show_help() {
  cat << 'EOF'
Repository Scout - Discover and manage git repos

USAGE:
  repo-scout [command] [options]

COMMANDS:
  scan [path] [depth]   Scan directory for git repos (default: ., depth 3)
  list                  List all discovered repos
  create [path] [name]  Create new git repo
  info [repo]           Show repo details
  status [repo]         Show repo status
  check [tool]          Check if tool is available
  cache-clear           Clear the repos cache
  help                  Show this help

EXAMPLES:
  repo-scout scan ~                    # Scan home directory
  repo-scout scan ~/projects 2         # Scan with depth limit
  repo-scout list                      # List cached repos
  repo-scout create ~/my-project MyApp # Create new repo
  repo-scout info ~/my-project         # Show repo info
  repo-scout status ~/my-project       # Show git status

NOTE: GitHub operations use the GitHub MCP server (equipped in rogue loadout)

EOF
}

# ============================================================================
# MAIN DISPATCHER
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
      create_repo "$2" "${3:-}"
      ;;
    info)
      show_repo_info "$2"
      ;;
    status)
      show_repo_status "$2"
      ;;
    check)
      if tool_exists "$2"; then
        log_success "$2 is available"
      else
        log_warn "$2 not found"
      fi
      ;;
    cache-clear)
      clear_cache
      ;;
    help|--help|-h)
      show_help
      ;;
    *)
      log_error "Unknown command: $cmd"
      show_help
      exit 1
      ;;
  esac
}

main "$@"
