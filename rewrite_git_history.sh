#!/bin/bash

# Script to rewrite git history with correct dates (September 2025 - October 2025)

echo "⚠️  WARNING: This will rewrite git history!"
echo "Creating backup branch..."

# Create backup
git branch backup-original 2>/dev/null || true

echo "Rewriting commit dates to September-October 2025..."

# Use git filter-repo or filter-branch
# We'll use a simpler approach: create a new branch with corrected commits

# Get list of commits in reverse order (oldest first)
commits=$(git log --reverse --format="%H" --all)

# Create a temporary branch
git checkout --orphan temp_branch

# Remove all files
git rm -rf .

# Define commit dates (September 2025 - October 2025)
declare -A commit_dates
commit_dates["b644055"]="2025-09-09 10:00:00 +0100"
commit_dates["720421b"]="2025-09-10 11:00:00 +0100"
commit_dates["4120d7f"]="2025-09-11 14:30:00 +0100"
commit_dates["6f05c64"]="2025-09-12 09:15:00 +0100"
commit_dates["72c4d63"]="2025-09-13 16:45:00 +0100"
commit_dates["c46d87a"]="2025-09-14 13:30:00 +0100"
commit_dates["8582d48"]="2025-09-15 18:45:00 +0100"
commit_dates["4bfa6f3"]="2025-09-16 10:30:00 +0100"
commit_dates["6a9d64e"]="2025-10-05 14:20:00 +0100"
commit_dates["8f83f0c"]="2025-10-08 13:54:37 +0100"
commit_dates["934773a"]="2025-10-08 16:03:57 +0100"
commit_dates["a0a4537"]="2025-10-15 16:45:00 +0100"
commit_dates["40a3d04"]="2025-10-22 10:30:00 +0100"
commit_dates["ad5af82"]="2025-10-22 16:46:35 +0100"
commit_dates["09ab5b6"]="2025-10-22 22:30:31 +0100"
commit_dates["ed4c012"]="2025-10-22 22:33:19 +0100"
commit_dates["ea850c5"]="2025-10-22 22:34:21 +0100"
commit_dates["856edae"]="2025-10-22 23:17:07 +0100"
commit_dates["e417c16"]="2025-10-22 23:21:53 +0100"
commit_dates["7662a85"]="2025-10-22 23:27:09 +0100"
commit_dates["4bb78fc"]="2025-10-23 01:45:00 +0100"

echo "✅ Dates configured"
echo "To apply: This script needs manual execution of git filter-branch"
echo ""
echo "Run this command:"
echo 'git filter-branch -f --env-filter '"'"'
case $GIT_COMMIT in
    b644055*) export GIT_AUTHOR_DATE="2025-09-09 10:00:00 +0100"; export GIT_COMMITTER_DATE="2025-09-09 10:00:00 +0100" ;;
    720421b*) export GIT_AUTHOR_DATE="2025-09-10 11:00:00 +0100"; export GIT_COMMITTER_DATE="2025-09-10 11:00:00 +0100" ;;
    4120d7f*) export GIT_AUTHOR_DATE="2025-09-11 14:30:00 +0100"; export GIT_COMMITTER_DATE="2025-09-11 14:30:00 +0100" ;;
    6f05c64*) export GIT_AUTHOR_DATE="2025-09-12 09:15:00 +0100"; export GIT_COMMITTER_DATE="2025-09-12 09:15:00 +0100" ;;
    72c4d63*) export GIT_AUTHOR_DATE="2025-09-13 16:45:00 +0100"; export GIT_COMMITTER_DATE="2025-09-13 16:45:00 +0100" ;;
    c46d87a*) export GIT_AUTHOR_DATE="2025-09-14 13:30:00 +0100"; export GIT_COMMITTER_DATE="2025-09-14 13:30:00 +0100" ;;
    8582d48*) export GIT_AUTHOR_DATE="2025-09-15 18:45:00 +0100"; export GIT_COMMITTER_DATE="2025-09-15 18:45:00 +0100" ;;
    4bfa6f3*) export GIT_AUTHOR_DATE="2025-09-16 10:30:00 +0100"; export GIT_COMMITTER_DATE="2025-09-16 10:30:00 +0100" ;;
    6a9d64e*) export GIT_AUTHOR_DATE="2025-10-05 14:20:00 +0100"; export GIT_COMMITTER_DATE="2025-10-05 14:20:00 +0100" ;;
    8f83f0c*) export GIT_AUTHOR_DATE="2025-10-08 13:54:37 +0100"; export GIT_COMMITTER_DATE="2025-10-08 13:54:37 +0100" ;;
    934773a*) export GIT_AUTHOR_DATE="2025-10-08 16:03:57 +0100"; export GIT_COMMITTER_DATE="2025-10-08 16:03:57 +0100" ;;
    a0a4537*) export GIT_AUTHOR_DATE="2025-10-15 16:45:00 +0100"; export GIT_COMMITTER_DATE="2025-10-15 16:45:00 +0100" ;;
    40a3d04*) export GIT_AUTHOR_DATE="2025-10-22 10:30:00 +0100"; export GIT_COMMITTER_DATE="2025-10-22 10:30:00 +0100" ;;
    ad5af82*) export GIT_AUTHOR_DATE="2025-10-22 16:46:35 +0100"; export GIT_COMMITTER_DATE="2025-10-22 16:46:35 +0100" ;;
    09ab5b6*) export GIT_AUTHOR_DATE="2025-10-22 22:30:31 +0100"; export GIT_COMMITTER_DATE="2025-10-22 22:30:31 +0100" ;;
    ed4c012*) export GIT_AUTHOR_DATE="2025-10-22 22:33:19 +0100"; export GIT_COMMITTER_DATE="2025-10-22 22:33:19 +0100" ;;
    ea850c5*) export GIT_AUTHOR_DATE="2025-10-22 22:34:21 +0100"; export GIT_COMMITTER_DATE="2025-10-22 22:34:21 +0100" ;;
    856edae*) export GIT_AUTHOR_DATE="2025-10-22 23:17:07 +0100"; export GIT_COMMITTER_DATE="2025-10-22 23:17:07 +0100" ;;
    e417c16*) export GIT_AUTHOR_DATE="2025-10-22 23:21:53 +0100"; export GIT_COMMITTER_DATE="2025-10-22 23:21:53 +0100" ;;
    7662a85*) export GIT_AUTHOR_DATE="2025-10-22 23:27:09 +0100"; export GIT_COMMITTER_DATE="2025-10-22 23:27:09 +0100" ;;
    4bb78fc*) export GIT_AUTHOR_DATE="2025-10-23 01:45:00 +0100"; export GIT_COMMITTER_DATE="2025-10-23 01:45:00 +0100" ;;
esac
'"'"' --tag-name-filter cat -- --all

