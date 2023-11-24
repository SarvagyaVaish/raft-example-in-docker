# syntax=docker/dockerfile:1

# Start with the pytorch image
FROM pytorch/pytorch:latest as base

# Install some basic packages
RUN apt-get update
RUN apt-get install -y git wget zip unzip vim

# Install CVML packages
RUN apt-get install -y libgl1-mesa-glx
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libglib2.0-0
RUN apt-get install libxcb-xinerama0
RUN pip install opencv-python
RUN pip install scipy

# Clone the RAFT repo and download the models
# Reference the readme from learnopencv for more details
#   https://github.com/spmallick/learnopencv/tree/master/Optical-Flow-Estimation-using-Deep-Learning-RAFT
RUN git clone https://github.com/MaximKuklin/RAFT.git
RUN ./RAFT/download_models.sh && rm models.zip

# Copy in the inference script
COPY ./inference.py ./
COPY ./data /default_data

# Run the interence. The output will show up in the ./data directory
CMD [ "python", "inference.py" ]

# Build the image using:
#   docker build -t raft-example .

# Run the container
#   Add "-it" to interact with the container
#   The "-v" mounts the host's relative "./data" directory to the absolute "/data" location
#   docker run --rm --platform linux/amd64 -v ./data:/data raft-example

# You're done! Check out the output in the local "./data" directory.
# You just ran RAFT int he docker container.
