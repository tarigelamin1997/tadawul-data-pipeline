# Use the official AWS Lambda Python image
FROM public.ecr.aws/lambda/python:3.11

# Copy requirements file
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install dependencies
RUN pip install -r requirements.txt

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY aws_secrets.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (file_name.function_name)
CMD [ "lambda_function.lambda_handler" ]