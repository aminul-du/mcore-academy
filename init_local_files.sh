#!/bin/bash
echo "📄 Creating local files..."

cat << 'F1' > 00-MASTER-CONTROL.md
# MCore Academy – Master Manifest
**Version:** 1.0
**Updated:** 22 July 2026
**Owner:** MCORE-FDR-AIS-001
**Framework:** MCore Academy Digital Knowledge OS
...
F1

cat << 'F2' > 01-KNOWLEDGE-INDEX.md
# MCore Academy – Knowledge Index
...
F2

cat << 'F3' > .gitignore
# Python
.venv/
venv/
*.pyc
...
F3

cat << 'F4' > README.md
# MCore Academy – Digital Knowledge Operating System
...
F4

cat << 'F5' > Makefile
.PHONY: help setup create_drive status
help:
	@echo "MCore Academy Commands:"
	@echo "  make setup        - Install Python dependencies"
	@echo "  make create_drive - Create Google Drive folders (Python)"
	@echo "  make status       - Check ecosystem status"
setup:
	pip install --user --upgrade google-api-python-client google-auth-oauthlib google-auth-httplib2
create_drive:
	python create_drive_folders.py
status:
	@echo "📊 MCore Academy Status:"
	@git remote -v | head -1
	@ls -la ~/.config/google-drive-mcp/ 2>/dev/null || echo "Not configured"
F5

echo "✅ All local files created."
