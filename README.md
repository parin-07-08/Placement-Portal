# Placement Portal Application

A multi-role placement management web application designed to streamline the interaction between students, companies, and administrators throughout the campus placement process.

## Overview

The Placement Portal provides a centralized platform for managing placement drives, student applications, company information, eligibility criteria, and placement-related reports.

The application supports different user roles and provides role-specific functionality for students, companies, and administrators.

## Key Features

### Student
- Student registration and authentication
- View available placement drives
- Check eligibility for placement opportunities
- Apply for eligible placement drives
- Track application status
- View application history

### Company
- Company registration and management
- Create and manage placement drives
- Define eligibility criteria
- View eligible student applications
- Track applicants and application statuses

### Administrator
- Manage students, companies, and placement drives
- Monitor placement activities
- View placement statistics and reports
- Manage application records
- Generate application and placement-related reports

### Background Processing
- Scheduled placement-related reports
- Asynchronous processing of data-intensive tasks
- Student application-history exports

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, Flask |
| Frontend | Vue.js |
| Database | SQLite |
| Caching | Redis |
| Background Tasks | Celery |
| API | Flask REST APIs |
| Data Format | JSON / CSV |

## System Architecture

The application follows a modular architecture consisting of:

```text
Frontend (Vue.js)
        |
        v
Flask REST API
        |
        +----------------+
        |                |
        v                v
    SQLite            Redis
                         |
                         v
                      Celery
                    Background
                       Tasks
