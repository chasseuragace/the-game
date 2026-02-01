#!/bin/bash

# Load Build - Equip a build and sync MCP servers
# This script handles the game mechanics of loading a build and configuring MCP

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly GAME_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly BUILDS_DIR="$GAME_ROOT/WORLD/builds"
readonly GEAR_DIR="$GAME_ROOT/WORLD/gear"
readonly CONFIG_DIR="$GAME_ROOT/WORLD/config"
readonly MCP_TEMPLATE="$CONFIG_DIR/mcp-template.json"
readonly MCP_CONFIG="$GAME_ROOT/.kiro/settings/mcp.json"
readonly CHARACTER_BUILD="$GAME_ROOT/CHARACTER/build.md"

# Colors
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

# ============================================================================
# BUILD LOADING
# ============================================================================

load_build() {
  local build_name="$1"
  
  [ -z "$build_name" ] && die "Build name required"
  
  local build_file="$BUILDS_DIR/$build_name/build.json"
  local gear_file="$GEAR_DIR/${build_name}_loadout.json"
  
  [ -f "$build_file" ] || die "Build not found: $build_name"
  [ -f "$gear_file" ] || die "Gear loadout not found: $build_name"
  
  log_info "⚔️  Loading build: $build_name"
  
  # Extract build info and write to CHARACTER/build.md
  extract_build_info "$build_file" "$build_name"
  
  # Sync MCP servers from gear loadout
  sync_mcp_servers "$gear_file"
  
  log_success "Build loaded: $build_name"
  log_info "MCP servers synced"
}

# ============================================================================
# BUILD INFO EXTRACTION
# ============================================================================

extract_build_info() {
  local build_file="$1"
  local build_name="$2"
  
  # Extract key info from build.json and write to CHARACTER/build.md
  cat > "$CHARACTER_BUILD" << EOF
# Active Build: $build_name

**Status:** Equipped

## Build Info

\`\`\`json
$(cat "$build_file" | head -20)
\`\`\`

---

*Loaded at: $(date)*
EOF
  
  log_success "Build info written to CHARACTER/build.md"
}

# ============================================================================
# MCP SERVER SYNCHRONIZATION
# ============================================================================

sync_mcp_servers() {
  local gear_file="$1"
  
  log_info "🔄 Syncing MCP servers from gear loadout..."
  
  # Extract mcpServers from gear loadout
  local mcp_servers
  mcp_servers=$(jq '.mcpServers' "$gear_file" 2>/dev/null || echo "{}")
  
  if [ "$mcp_servers" = "{}" ]; then
    log_warn "No MCP servers defined in gear loadout"
    return 0
  fi
  
  # Merge with existing workspace MCP config
  merge_mcp_config "$mcp_servers"
}

merge_mcp_config() {
  local new_servers="$1"
  
  # Start with template (includes voice MCP)
  local base_config
  if [ -f "$MCP_TEMPLATE" ]; then
    base_config=$(cat "$MCP_TEMPLATE")
  else
    die "MCP template not found: $MCP_TEMPLATE"
  fi
  
  # Filter out disabled MCPs from new_servers before merging
  local filtered_servers
  filtered_servers=$(echo "$new_servers" | jq 'with_entries(select(.value.disabled != true))')
  
  # Merge new servers into template, respecting disabled flags
  local merged
  merged=$(echo "$base_config" | jq ".mcpServers += $filtered_servers")
  
  # Also filter out any disabled MCPs from the final result
  merged=$(echo "$merged" | jq '.mcpServers |= with_entries(select(.value.disabled != true))')
  
  # Write to workspace config
  mkdir -p "$(dirname "$MCP_CONFIG")"
  echo "$merged" | jq '.' > "$MCP_CONFIG"
  
  log_success "MCP servers synced to workspace config (voice MCP always equipped, disabled MCPs filtered)"
}

# ============================================================================
# VALIDATION
# ============================================================================

validate_environment() {
  command -v jq &> /dev/null || die "jq is required but not installed"
  [ -d "$BUILDS_DIR" ] || die "Builds directory not found: $BUILDS_DIR"
  [ -d "$GEAR_DIR" ] || die "Gear directory not found: $GEAR_DIR"
  [ -f "$MCP_TEMPLATE" ] || die "MCP template not found: $MCP_TEMPLATE"
}

# ============================================================================
# MAIN
# ============================================================================

main() {
  local build_name="${1:-}"
  
  if [ -z "$build_name" ]; then
    log_error "Usage: load-build.sh [build-name]"
    echo ""
    echo "Available builds:"
    ls -1 "$BUILDS_DIR" 2>/dev/null | sed 's/^/  - /'
    exit 1
  fi
  
  validate_environment
  load_build "$build_name"
}

main "$@"
