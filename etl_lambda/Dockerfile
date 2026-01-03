# Use the official AWS Lambda Python image
FROM public.ecr.aws/lambda/python:3.11

# Copy requirements
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install dependencies (ensure numpy<2.0.0 is in requirements.txt)
RUN pip install -r requirements.txt

# --- UPDATED: COPY BOTH SCRIPTS ---
COPY ingest.py ${LAMBDA_TASK_ROOT}
COPY process.py ${LAMBDA_TASK_ROOT}
COPY aws_secrets.py ${LAMBDA_TASK_ROOT}

# Default CMD (can be overridden in Lambda Console)
CMD [ "ingest.lambda_handler" ]