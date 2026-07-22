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
