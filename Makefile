# AI Content Generation Suite Makefile

.PHONY: install-dev test-all build-all clean format lint

# Install all packages in development mode
install-dev:
	@echo "🔧 Installing all packages in development mode..."
	@find packages -name "setup.py" -exec dirname {} \; | while read dir; do \
		echo "Installing $$dir..."; \
		pip install -e $$dir; \
	done

# Run tests for all packages
test-all:
	@echo "🧪 Running tests for all packages..."
	@find packages -name "tests" -type d | while read testdir; do \
		echo "Testing $$testdir..."; \
		cd "$$(dirname $$testdir)" && python -m pytest tests/; \
	done

# Build all packages
build-all:
	@echo "📦 Building all packages..."
	@find packages -name "setup.py" -exec dirname {} \; | while read dir; do \
		echo "Building $$dir..."; \
		cd $$dir && python -m build; \
	done

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true

# Format code
format:
	@echo "🎨 Formatting code..."
	@black packages/
	@isort packages/

# Lint code
lint:
	@echo "🔍 Linting code..."
	@flake8 packages/
	@black --check packages/
	@isort --check-only packages/
