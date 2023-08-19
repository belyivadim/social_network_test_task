FROM python:3.10.0

# set the working directory inside the container
WORKDIR /usr/src/app

# copy requirements
COPY requirements.txt ./

# Install deps
RUN pip install -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port on which app is listening
EXPOSE 8080


CMD ["python3", "src/app.py"]

