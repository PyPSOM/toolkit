!/bin/bash

# Install zlib
# Build and install zlib
v=1.2.8  
wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4/zlib-${v}.tar.gz
tar -xf zlib-${v}.tar.gz && cd zlib-${v}
ZDIR=/usr/local/zlib
./configure --prefix=${ZDIR}
make check
make install   # or sudo make install, if root permissions required
cd .. && rm zlib-${v}.tar.gz && rm -rf zlib-${v}

# Install HDF5
v=1.8.13
wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4/hdf5-${v}.tar.gz
tar -xf hdf5-${v}.tar.gz && cd hdf5-${v}
# Build and install HDF5
H5DIR=/usr/local/hdf
./configure --with-zlib=${ZDIR} --prefix=${H5DIR} --enable-hl --enable-parallel
make check
make install   # or sudo make install, if root permissions required
cd .. && rm hdf5-${v}.tar.gz && rm -rf hdf5-${v}

# Install Netcdf
v=4.1.3
wget http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-${v}.tar.gz
tar -xf netcdf-${v}.tar.gz && cd netcdf-${v}
# Build and install netCDF-4
NCDIR=/usr/local/netcdf
CPPFLAGS='-I${H5DIR}/include -I${ZDIR}/include' LDFLAGS='-L${H5DIR}/lib -L${ZDIR}/lib' ./configure --disable-netcdf-4 --disable-shared --enable-parallel-tests --prefix=${NCDIR}
make check
make install  # or sudo make installe install
cd .. && rm netcdf-${v}.tar.gz && rm -rf netcdf-${v}