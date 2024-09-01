# select python image
FROM python:3.10

# Add non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && apt-get clean

# Update package lists
RUN apt-get update && \
    apt-get -y upgrade

# Install Google Cloud CLI
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && apt-get update -y && apt-get install google-cloud-sdk -y

# Set the working directory in the container
WORKDIR /workspace

# Copy requirements file
COPY requirements.txt requirements.txt

# Install pip
RUN pip install --no-cache-dir --upgrade pip

# Install pipenv
RUN pip install pipenv

# Expose the port the app runs on
EXPOSE 8000

# Set user
USER $USERNAME

# Run any command to initialize the container
CMD ["bash"]
