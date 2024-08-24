# Define the virtual environment directory
VENV_DIR := venv

# Define the Python interpreter
PYTHON := $(VENV_DIR)/bin/python

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
	@. $(VENV_DIR)/bin/activate

# Run app.py using the virtual environment
run:
	@. $(VENV_DIR)/bin/activate && python ./src/main.py