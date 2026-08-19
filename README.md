# AWS Linux Support Lab

A hands-on cloud support project demonstrating how a Python web service can be containerised with Docker, deployed to an AWS EC2 Linux server, monitored, troubleshot, and recovered after failure or reboot.

## Project Objective

The goal of this project was to practise practical Linux, Docker, networking, AWS, and troubleshooting skills in a realistic cloud environment rather than only learning commands in isolation.

## Architecture

Mac
→ SSH / SCP
→ AWS EC2 (Amazon Linux 2023)
→ Docker
→ FastAPI application
→ Port 8000
→ `/health` endpoint

## Technologies Used

- AWS EC2
- Amazon Linux 2023
- Docker
- FastAPI
- Uvicorn
- Linux CLI
- SSH / SCP
- Git

## Application

The FastAPI service provides a simple health endpoint:

```text
GET /health
