# Todo List Application

## Overview

A simple todo list web application built with Streamlit and PostgreSQL. The app allows users to create, manage, and track todo items with support for priorities and due dates.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend
- **Streamlit** serves as both the UI framework and web server
- Single-page application with a centered layout
- No separate frontend build process required - Streamlit handles rendering

### Backend
- **Python** application with Streamlit handling HTTP requests
- Database operations performed directly through psycopg2 (PostgreSQL adapter)
- No separate API layer - database calls happen inline with UI logic

### Data Storage
- **PostgreSQL** database for persistent storage
- Single `todos` table with fields:
  - `id` - Auto-incrementing primary key
  - `text` - Todo item content
  - `completed` - Boolean completion status
  - `priority` - String field (Low/Medium/High)
  - `due_date` - Optional date field
  - `created_at` - Timestamp for ordering

### Design Patterns
- Direct database connection per operation (no connection pooling)
- Database initialization runs on app startup with idempotent table creation
- Environment variable (`DATABASE_URL`) for database configuration

## External Dependencies

### Database
- **PostgreSQL** - Primary data store, connected via `DATABASE_URL` environment variable

### Python Packages
- **streamlit** - Web framework and UI
- **psycopg2** - PostgreSQL database adapter