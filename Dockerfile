FROM nvidia/cuda:12.3.1-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY :0
ENV QT_X11_NO_MITSHM=1
ENV PYTHONPATH=/workspace
RUN ln -snf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && echo Asia/Tokyo > /etc/timezone
ENV XDG_RUNTIME_DIR=/tmp/runtime-evodiffusion


RUN apt-get update && apt-get install -y \
    sudo \
    wget \
    git \
    vim 

RUN sudo apt-get install -qq -y \
        libfontconfig1 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-render-util0 \
        libxcb-shape0 \
        libxcb-xinerama0 \
        libxcb-xkb1 \
        libsm6 \
        libxkbcommon-x11-0 \
        libdbus-1-3 \
        libfreetype6 \ 
        libxcb1 \       
        libgl1-mesa-glx \
        libglib2.0-0 

WORKDIR /opt

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    sh Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda3 && \
    rm -r Miniconda3-latest-Linux-x86_64.sh

ENV PATH /opt/miniconda3/bin:$PATH

RUN pip install --upgrade pip && \
    conda update -n base -c defaults conda && \
    conda create -y -n ex_env python=3.10

# # ex_env環境をアクティベートするコマンドを.bashrcに追加
# RUN echo "source activate ex_env" >> ~/.bashrc

SHELL ["conda", "run", "-n", "ex_env", "/bin/bash", "-c"]

RUN conda install -y pytorch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 pytorch-cuda=12.1 -c pytorch -c nvidia && \
    pip install diffusers transformers accelerate --upgrade 

RUN pip install PyQt5 

WORKDIR /

CMD ["conda", "run", "-n", "ex_env", "/bin/bash"]

