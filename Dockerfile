# Step 1: Use an official Python runtime as a parent image
# Using a slim version to keep the image size down
FROM python:3.12-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy dependency files and install them
# This is done in a separate step to leverage Docker's layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the rest of the application's code into the container
# This includes the api/, db/, etl/, and utils/ directories
COPY . .

# Step 5: Command to run when the container launches
# This tells uvicorn to run the app defined in api/main.py
# --host 0.0.0.0 makes it accessible from outside the container
# --port 8080 is a standard cloud port
CMD ["./start.sh"]
