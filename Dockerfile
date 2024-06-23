FROM python:3.10-slim as build

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install poetry==1.8.3

# Install dependencies
RUN poetry install

# Build the application
RUN poetry build

# Create a new stage for the runtime image
FROM python:3.10-slim as runtime

# Set the working directory
WORKDIR /app

# Copy the build artifacts from the build stage
COPY --from=build /app/dist /app/dist

# Install the application
RUN pip install /app/dist/*.whl

# Remove the build artifacts
RUN rm -rf /app/dist
