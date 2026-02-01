# Shell MCP Playground - Exercises

## Exercise 1: Basic Commands
Try these commands in the shell MCP:

```bash
# List files
ls -la

# Show current directory
pwd

# Show file contents
cat data/sample.txt

# Count lines
wc -l data/sample.txt
```

## Exercise 2: Text Processing
Practice with grep and basic text manipulation:

```bash
# Search for a pattern
grep "Seattle" data/sample.csv

# Count occurrences
grep -c "Engineer" data/sample.csv

# Show line numbers
grep -n "line" data/sample.txt
```

## Exercise 3: Piping
Chain commands together:

```bash
# Count total lines
cat data/sample.txt | wc -l

# Filter and count
grep "Seattle" data/sample.csv | wc -l

# Sort and display
sort data/sample.csv | head -3
```

## Exercise 4: File Operations
Create and manipulate files:

```bash
# Create a new file
echo "Hello from shell MCP" > test_output.txt

# Append to file
echo "Line 2" >> test_output.txt

# Display file
cat test_output.txt

# Copy file
cp test_output.txt test_output_backup.txt
```

## Exercise 5: Advanced Piping
Combine multiple commands:

```bash
# Extract and count
cat data/sample.csv | cut -d',' -f3 | sort | uniq -c

# Filter and format
grep "Engineer" data/sample.csv | cut -d',' -f1,3

# Multi-step processing
cat data/sample.csv | tail -n +2 | cut -d',' -f2 | sort -n
```

---

*Work through these exercises to master the shell MCP*
