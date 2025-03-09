# Use a lightweight image of python:3.11
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy frontend files to the working directory
COPY . .

# Expose the frontend port
EXPOSE 8001

# Run the frontend server
CMD ["python", "-m", "http.server", "8001"]