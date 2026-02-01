# Shell MCP Playground

A safe space to explore and test the shell MCP capabilities.

## What is the Shell MCP?

The shell MCP (mcp-shell) provides secure terminal command execution through the Model Context Protocol. It allows you to run shell commands and capture their output.

## Getting Started

### Basic Commands to Try

```bash
# List files in current directory
ls -la

# Check current working directory
pwd

# Show system information
uname -a

# List environment variables
env

# Check disk usage
df -h

# Show current date/time
date

# Count lines in a file
wc -l README.md

# Search for patterns
grep -r "test" .

# Create test files
echo "Hello from shell MCP" > test.txt

# Chain commands
cat test.txt | wc -c
```

### Playground Structure

- `test.txt` - Sample test file
- `scripts/` - Shell scripts to experiment with
- `data/` - Sample data files for processing

## Learning Path

1. **Basic Execution** - Run simple commands (ls, pwd, echo)
2. **File Operations** - Create, read, modify files
3. **Text Processing** - Use grep, awk, sed
4. **Piping** - Chain commands together
5. **Scripts** - Write and execute shell scripts

## Notes

- All commands execute in this playground directory
- Output is captured and returned
- Errors are handled gracefully
- Use this space to experiment safely

---

*Created for Rogue Tier 1 training - Shell MCP Mastery*
