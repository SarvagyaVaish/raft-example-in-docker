# About The Project

This repo is a dockerized example of Optical Flow using [RAFT](https://github.com/princeton-vl/RAFT). This is adapted from the LearnOpenCV [blog post](https://learnopencv.com/optical-flow-using-deep-learning-raft/) and [Github repo](https://github.com/spmallick/learnopencv/tree/master/Optical-Flow-Estimation-using-Deep-Learning-RAFT).

I was hoping to very quickly test out RAFT for my use case, but ended up spending a significant amount of time just setting up the environment. If you're in the same boat, I hope this Docker image makes it easy for you.

  

# Usage

## Short version

1. Clone this repo

2. Put two images (`frame_1.png`, `frame_2.png`) in the `data` folder

3. Build the Docker image

4. Run the Docker image and mount the `./data` directory to `/data` in the container

5. 🎉 Result will be saved in the `data` directory


## Detailed version with commands

1. Install [Docker](https://docs.docker.com/engine/install/). You can check your installation using
    ```sh
    docker info
    ```

2. Clone this repo

    ```sh
    git clone https://github.com/SarvagyaVaish/raft-example-in-docker.git
    cd raft-example-in-docker
    ```

3. Add two images to `./data` (optional)

    There are two sample images already provided. So if you want you can skip this step. If you do decide to add your own images, make sure they are named `frame_1.png` and `frame_2.png`. I know, this is janky! See [Roadmap](#roadmap) for improvements for what's coming up, and [Contributing](#contributing) for how you can help.

    ```sh
    cp ./path/to/my/frame_1.png ./data/frame_1.png
    cp ./path/to/my/frame_2.png ./data/frame_2.png
    ```

4. Build the docker image from the provided `Dockerfile`

    I call my image `raft-example`. It's based on the `pytorch/pytorch` image from [Docker Hub](https://hub.docker.com/r/pytorch/pytorch).

    ```sh
    docker build -t raft-example .
    ```

    Option to Pull a Docker image coming soon! See [Roadmap](#roadmap).

5. Run the `raft-example` image

    It will process the two frames located in `./data` and output a timestamped result image showing the optical flow field. See [Flow Vis](https://github.com/tomrunia/OpticalFlow_Visualization) to interpret the colors. TLDR, it assigns a color based on the direction of the optical flow vector.

    ```sh
    docker run --rm --platform linux/amd64 -v ./data:/data raft-example
    ```

    - The "-v" argument is important! It mounts the host's relative "./data" directory to the absolute "/data" location.
    - Add the "-it" argument to interact with the container via the command line.

6. 🎉 Done!

    Results are timestamped and saved in the local `./data` directory.

  

<!-- ROADMAP -->
## Roadmap

- [ ] Video walkthrough
- [ ] Docker pull option
- [ ] Remove the image naming constraints (`frame_1.png`, ...)
- [ ] Add ability to process video

  

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
