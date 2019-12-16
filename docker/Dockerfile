FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y python3
RUN apt-get install -y git
RUN apt-get install -y curl 
RUN apt-get install -y bash 
RUN apt-get install -y gfortran
RUN apt-get install -y vim
RUN apt-get install -y libnetcdf-dev libnetcdff-dev
RUN apt-get install -y xutils-dev

COPY dependencies/* /tmp/install_netcdf/dependencies/
COPY ./install_netcdf.sh /tmp/install_netcdf/install.sh
WORKDIR /tmp/install_netcdf
RUN bash install.sh

# Add GOTM Dependendicies
RUN apt-get install -y cmake
RUN mkdir -p /tmp/gotmbuild && mkdir -p /tmp/gotmsource
WORKDIR /tmp/gotmsource
ENV GOTM_BASE="/tmp/gotmsource/code"
RUN git clone -q --recursive https://github.com/gotm-model/code.git
WORKDIR /tmp/gotmbuild
RUN $GOTM_BASE/scripts/linux/gotm_configure.sh 
RUN $GOTM_BASE/scripts/linux/gotm_build.sh
ENV PATH="/root/local/gotm/gfortran/bin:${PATH}"

# Delete of unnecessary dependencies
RUN rm -rf ${GOTM_BASE}
RUN apt-get remove --purge -y wget
RUN apt-get remove --purge -y python3
RUN apt-get remove --purge -y git
RUN apt-get remove --purge -y curl 

WORKDIR /usr/temp/pypsom/code

ENTRYPOINT ["bash"]
CMD [ ]

LABEL Author="PyPSOM Team"
LABEL version="0.63.1"
