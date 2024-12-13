#!/bin/bash

# Exit on any error
set -e

# Run database migrations
flask db upgrade

# Start the application
gunicorn run:app