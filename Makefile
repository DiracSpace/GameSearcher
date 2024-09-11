# Define the virtual environment directory
VENV_DIR := venv

# Detect OS and set the Python interpreter path accordingly
ifeq ($(OS),Windows_NT)
    PYTHON := $(VENV_DIR)/Scripts/python.exe
    ACTIVATE := $(VENV_DIR)/Scripts/activate
else
    PYTHON := $(VENV_DIR)/bin/python
    ACTIVATE := $(VENV_DIR)/bin/activate
endif

# Create the virtual environment and install dependencies
install:
	python -m venv $(VENV_DIR)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install --progress-bar on -r requirements.txt

# Clean up the virtual environment
clean:
	rm -rf $(VENV_DIR)

# Activate the virtual environment
activate:
	@. $(ACTIVATE)

# Run app.py using the virtual environment
run:
	make activate && uvicorn backend.server:app --reload --port 8000

# Run tests
test:
	make activate && $(PYTHON) -m unittest discover -s .\tests\ -p 'test_*.py'