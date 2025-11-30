#!/bin/bash
cd /home/vikas/Desktop/adgenesis/backend
./venv/bin/python -m uvicorn app.main:app --reload --port 8000
