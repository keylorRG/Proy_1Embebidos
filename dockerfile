ARG OS_VER="2023.0.0-ubuntu22-gpu682-dpcpp-devel"
FROM intel/dlstreamer:${OS_VER}

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git \
        libgstreamer1.0-dev \
        libgstreamer-plugins-base1.0-dev

# Uninstall the current OpenCV module
RUN pip3 uninstall -y opencv-python

RUN apt-get update && apt-get install -y \
	libgtk2.0-dev \
	pkg-config

# Build OpenCV 4.7.0 with GStreamer support
RUN git clone https://github.com/opencv/opencv.git && \
    cd opencv && git checkout 4.7.0 && \
    mkdir build && cd build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D WITH_GSTREAMER=ON \
        -D WITH_GTK=ON \ #para la interfaz
        -D BUILD_opencv_python3=yes \
        -D PYTHON_EXECUTABLE=$(which python3) .. && \
    make -j$(nproc) && \
    make install && \
    cd ../../ && rm -rf opencv

USER dlstreamer

# Install only essential Python dependencies
RUN pip3 install pillow matplotlib

# Download only the human pose estimation model we need
RUN mkdir -p models && cd models && \
    omz_downloader --name human-pose-estimation-0001 --precisions FP32


