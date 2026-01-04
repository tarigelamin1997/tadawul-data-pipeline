📈 Event-Driven Financial Data Pipeline & Dashboard
A robust, end-to-end cloud engineering project that automates the ingestion, processing, storage, and visualization of high-frequency financial market data using a serverless, event-driven architecture.

🖼️ Project Overview
This project represents a modern Cloud-Native Data Pipeline designed to track US Tech stocks (TSLA, AAPL, NVDA). Unlike traditional static dashboards, this system utilizes an Event-Driven Architecture where data ingestion triggers automated processing workflows in the cloud.

The goal was to move beyond simple scripts and build a production-grade system that handles the full lifecycle of data: from raw API extraction to persistent storage in a relational database, served via a containerized frontend application.

🎯 Key Features
Real-Time Visualization: Interactive charts built with Plotly & Streamlit showing multi-year price history.

Event-Driven ETL: Data processing is triggered automatically by S3 upload events (Serverless).

Automated CI/CD: Zero-touch deployment pipeline using GitHub Actions and AWS Elastic Beanstalk.

Containerized Environment: Fully Dockerized application ensuring consistency between development and production.

Secure Infrastructure: Database credentials and API keys managed via environment variables and GitHub Secrets.

🏗️ System Architecture
The system follows a microservices-inspired flow, separating concerns between extraction, transformation, storage, and presentation.

graph LR
    A[External API] -->|Fetch Data| B(AWS Lambda / Script)
    B -->|Upload Raw JSON| C[AWS S3 Bucket]
    C -->|S3 Event Trigger| D[ETL Processor (Lambda)]
    D -->|Clean & Transform| E[(AWS RDS PostgreSQL)]
    E -->|Query Data| F[Streamlit Dashboard]
    F -->|Serve| G[End User]
    style F fill:#00C853,stroke:#333,stroke-width:2px
    style E fill:#3F51B5,stroke:#333,stroke-width:2px

Ingestion: A fetcher script retrieves market data and deposits raw JSON files into an AWS S3 bucket.

Processing (ETL): An AWS Lambda function is triggered immediately upon file upload. It parses the JSON, validates schema, and cleans the data.

Storage: Cleaned data is upserted into an AWS RDS (PostgreSQL) database, ensuring ACID compliance and data integrity.

Deployment: The frontend dashboard is packaged as a Docker container and deployed to AWS Elastic Beanstalk.

🛠️ Technical Stack
Cloud Infrastructure (AWS)
Elastic Beanstalk (Docker Platform): Orchestrates the deployment of the dashboard application.

RDS (PostgreSQL): Managed relational database service for persistent storage.

S3 (Simple Storage Service): Data lake for raw JSON ingestion.

Lambda (Serverless): Compute service for event-driven ETL tasks.

Application Layer
Python 3.11: Core programming language.

Streamlit: Framework for the interactive web interface.

Plotly Graph Objects: Advanced data visualization library.

SQLAlchemy: ORM for secure and efficient database interactions.

Pandas: High-performance data manipulation and analysis.

DevOps & Tooling
Docker: Containerization for reproducible builds (Multi-stage builds).

GitHub Actions: CI/CD pipeline for automated testing and deployment.

Git: Version control with branching strategies.

🚀 Deployment & CI/CD Pipeline
The project utilizes a Continuous Deployment strategy. Every commit to the main branch triggers a GitHub Actions workflow that automatically updates the production server.

Workflow Steps (deploy.yml):

Checkout Code: Pulls the latest code from the repository.

Generate Deployment Package: Compresses the application (excluding virtual environments and unnecessary files).

Deploy to AWS: Uses the einaregilsson/beanstalk-deploy action to push the zip file to Elastic Beanstalk.

Version Management: Handles versioning automatically using Git commit hashes.

Note: The pipeline includes safety checks (e.g., use_existing_version_if_available) to prevent deployment failures during rapid iterations.

💻 Local Development Setup
To run this project locally, follow these steps:

Prerequisites
Docker Desktop installed

Python 3.11+

Git

Installation
1. Clone the repository:
git clone https://github.com/YourUsername/tadawul-data-pipeline.git
cd tadawul-data-pipeline

2. Set up Environment Variables Create a .env file in the root directory:
DB_USER=postgres
DB_PASS=your_password
DB_HOST=localhost
DB_NAME=tadawul

3. Run with Docker
docker build -t tech-dashboard .
docker run -p 8501:8501 --env-file .env tech-dashboard

4. Access the Dashboard Open your browser and navigate to http://localhost:8501

🛡️ Engineering Challenges & Solutions
During development, several critical engineering challenges were solved:

1. Cross-Platform Dependency Management ("Dependency Hell")
Problem: The local environment (Windows) produced a requirements.txt with dependencies incompatible with the AWS Linux environment (e.g., pywin32, specific binary wheels), causing the build to fail with Exit Code 1.

Solution: Implemented a clean-slate strategy for requirements. Instead of freezing the entire local environment, I curated a minimal requirements.txt listing only top-level dependencies. This allows the Docker container to resolve and compile the correct Linux-compatible binaries during the build process.

2. The "Ghost" Deployment (Git Indexing)
Problem: eb deploy reported success, but the production site showed old code. This was because the deployment tool relies on the Git Index, not the local file system.

Solution: Established a strict workflow of Stage -> Commit -> Push before deployment, ensuring the CI/CD pipeline always picks up the latest committed changes.

3. Library Stability vs. Novelty
Problem: Attempting to use beta versions of financial libraries (pandas-ta) and bleeding-edge numpy (v2.0+) caused internal conflict crashes in the Docker container.

Solution: Prioritized System Stability. I engineered the requirements.txt to pin numpy<2.0.0 to ensure compatibility and removed unstable beta libraries, opting for robust, standard implementation of moving averages using native Pandas functions.

🔮 Future Improvements
Alerting System: Integrate AWS SNS to send SMS/Email alerts when a stock crosses a "Golden Cross" threshold.

IaC (Infrastructure as Code): Migrate manual AWS setup to Terraform or CloudFormation scripts.

Unit Testing: Add pytest suite to the CI pipeline to validate data integrity before deployment.

👨‍💻 Author
Tarig Elamin

Cloud Engineer | Data Engineer

Specializing in Python, AWS, and DevOps Automation.

LinkedIn Profile: www.linkedin.com/in/tarigelamin

📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.