# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port for Streamlit
EXPOSE 8501

# Run the synthetic data generator, then ETL, then start Streamlit
CMD ["sh", "-c", "python scripts/generate_mock_data.py && python src/etl_pipeline.py && streamlit run app/dashboard.py --server.port=8501 --server.address=0.0.0.0"]