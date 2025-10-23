#!/bin/bash
pkill -f "python.*app.py"
source venv_new/bin/activate
python app.py
