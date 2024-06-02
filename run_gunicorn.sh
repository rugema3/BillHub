# Run gunicorn in the background. 
gunicorn -w 2 -b 0.0.0.0:8000 -D app:app
