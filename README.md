# Requirements to Design - R2D 
[![R2D Django-React CI](https://github.com/Yapping72/R2D/actions/workflows/r2d-django-react-ci.yml/badge.svg?branch=main)](https://github.com/Yapping72/R2D/actions/workflows/r2d-django-react-ci.yml)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Django Rest Framework](https://img.shields.io/badge/Django%20Rest%20Framework-3.14%2B-green)
![React](https://img.shields.io/badge/React-18.2.0%2B-blue)

## Demo
* Video Demo: https://youtu.be/8UXmJH2IrHw
* [Presentation Slides](documentation/presentation_slides.pdf)

## **ICT4001 Capstone Project Yap Ping 2101074 Requirements To Design (R2D)** 

The Requirements to Design (R2D) capstone project was conceived to streamline requirement interpretation, improve documentation consistency, and enhance communication between technical and non-technical stakeholders. The primary purpose of the application is to streamline the interpretation of requirements in the form of user stories to dynamically generate appropriate Unified Modelling Language (UML) diagrams. R2D will support basic modification of diagrams and integrate seamlessly with Draw.io to allow comprehensive diagram modifications.

R2D aims to achieve the following goals:

**1. Streamlining interpretation of functional requirements**: By converting functional requirements to UML diagrams, stakeholders can gain greater clarity and insights.

**2. Bridging gaps between stakeholders**: R2D can rapidly generate ideas to diagrams to facilitate the brainstorming and solutioning process.

**3. Increase developer productivity**: Developers and analyst within Accenture are responsible for documenting and generating diagrams for their created components. This task is time-consuming and takes up significant man-hours. R2D can alleviate this issue by generating a base-template for developers to work on

**4. Breaking communication barriers**: UML diagrams transcend language boundaries and is a concrete strategy to effectively minimize language barriers, facilitating seamless communication and understanding among team members from various linguistic backgrounds.

## Technology Stack
R2D was developed using React Frontend and Python Django Framework as backend with Postgres serving as the primary database. Redis and Celery workers were also incorporated to achieve distributed processing when interfacing with LLMs (LangChain).

![Stack](https://raw.githubusercontent.com/Yapping72/R2D/main/documentation/stack.png)

## Overview of Processing Framework

![Stack](https://raw.githubusercontent.com/Yapping72/R2D/main/documentation/overview.png)

## Project Structure
The project directory is organized as follows:
* [**django_backend_r2d**](django_backend_r2d): This directory contains the Django backend code.
* [**jenkins**](jenkins): This directory is used for Jenkins CI/CD configurations (if applicable).
* [**react_frontend_r2d**](react_frontend_r2d): This directory contains the React frontend code.
* [**aws_configuration**](aws_configuration): This directory contains AWS configuration files e.g., UserData scripts, IAM policies etc.


# Build Application
1. ```` docker compose build ````
2. ```` docker compose up ````
3. R2D web pages deployed on port 5173.
