#!/bin/bash

# Setup script for Atomic Limits Research Repository
# This script initializes a git repository and optionally pushes to GitHub

set -e  # Exit on error

echo "========================================"
echo "Atomic Limits Research - Repository Setup"
echo "========================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: git is not installed"
    echo "Install git first: https://git-scm.com/downloads"
    exit 1
fi

echo "✓ Git is installed"
echo ""

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already exists"
fi

# Add all files
echo ""
echo "Adding files to git..."
git add .

# Create initial commit
echo ""
echo "Creating initial commit..."
if git diff --cached --quiet; then
    echo "⚠ No changes to commit (repository may already be set up)"
else
    git commit -m "Initial commit: Atomic stability limits and exceptional mathematics research

- Complete verification script (verify_atomic_limits.py)
- Full documentation (atomic_limits_exceptional_math.md)
- Research roadmap with 4 investigation paths
- Authoritative sources and verification links
- Quick start guide for immediate use

Core finding: Physical atomic stability limits (92, 137, 173) encode
exceptional mathematical dimensions (8, 22-24, 43) through their
decimal period structure."
    echo "✓ Initial commit created"
fi

# Check for GitHub CLI
echo ""
if command -v gh &> /dev/null; then
    echo "✓ GitHub CLI (gh) detected"
    echo ""
    read -p "Create GitHub repository and push? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Repository name (default: atomic-limits-research): " REPO_NAME
        REPO_NAME=${REPO_NAME:-atomic-limits-research}
        
        read -p "Make repository public? (y/N): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            VISIBILITY="--public"
        else
            VISIBILITY="--private"
        fi
        
        echo ""
        echo "Creating GitHub repository: $REPO_NAME"
        gh repo create "$REPO_NAME" $VISIBILITY --source=. --remote=origin
        
        # Check if main branch exists, if not create it
        if ! git show-ref --verify --quiet refs/heads/main; then
            git branch -M main
        fi
        
        echo "Pushing to GitHub..."
        git push -u origin main
        
        echo ""
        echo "✓ Repository created and pushed to GitHub!"
        echo ""
        gh repo view --web
    fi
else
    echo "ℹ GitHub CLI not found"
    echo ""
    echo "To push to GitHub manually:"
    echo ""
    echo "1. Create a new repository at: https://github.com/new"
    echo "2. Then run these commands:"
    echo ""
    echo "   git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
fi

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Run verification:"
echo "   python3 verify_atomic_limits.py"
echo ""
echo "2. Read the quick start guide:"
echo "   cat QUICKSTART.md"
echo ""
echo "3. Explore the research roadmap:"
echo "   cat research_roadmap.md"
echo ""
echo "4. Check authoritative sources:"
echo "   cat authoritative_sources.md"
echo ""
echo "Happy researching! 🔬"
echo ""
