# Car Charging Reservation System

## Running Locally with Python

1. Install Python 3.13 and pip, or uv.

2. Install dependencies with:

- pip:
  ```bash
  cd backend
  python -m venv .venv
  source .venv/bin/activate
  pip install pyproject.toml
  ```
- uv:
  ```bash
   cd backend
   uv venv
   source .venv/bin/activate
   uv sync
  ```

3. Run the application:
   ```bash
   python src/main.py
   ```
4. Visit [http://localhost:8080](http://localhost:8080) in your browser.

## Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t car-charging-backend ./backend
   ```
2. Run the container:
   ```bash
   docker run -p 8080:8080 car-charging-backend
   ```
3. Visit [http://localhost:8080](http://localhost:8080) in your browser.

---

For development, make sure to restart the server after code changes if not using `--reload`.
