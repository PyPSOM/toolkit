#### COPY TO install.sh ###
#!/bin/bash

# VERY BASIC installation script of required libraries
# for installing these packages:
#   zlib-1.2.8
#   hdf5-1.8.14
#   netcdf-4.3.3
#   netcdf-fortran-4.4.1

# If you have downloaded other versions edit these version strings
z_v=1.2.8
h_v=1.8.14
nc_v=4.3.3
nf_v=4.4.1

# Install path, change accordingly
# You can change this variable to control the installation path
# If you want the installation path to be a "packages" folder in
# your home directory, change to this:
ID="/tmp/netcdf/packages/"
DEPENDENCIES="/tmp/install_netcdf/dependencies/"

#################
# Install z-lib #
#################
cd $DEPENDENCIES
tar xfz zlib-${z_v}.tar.gz
cd zlib-${z_v}
./configure --prefix $ID/zlib/${z_v}
make
make test 2>&1 | tee zlib.test
make install
mv zlib.test $ID/zlib/${z_v}/
cd ../
rm -rf zlib-${z_v}
rm zlib-${z_v}.tar.gz
echo "Completed installing zlib"
[ -d $ID/zlib/${z_v}/lib64 ] && zlib_lib=lib64 || zlib_lib=lib

################
# Install hdf5 #
################
tar xfz hdf5-${h_v}.tar.gz
cd hdf5-${h_v}
mkdir build ; cd build
../configure --prefix=$ID/hdf5/${h_v} \
	--enable-shared --enable-static \
	--enable-fortran --with-zlib=$ID/zlib/${z_v} \
	LDFLAGS="-L$ID/zlib/${z_v}/$zlib_lib -Wl,-rpath=$ID/zlib/${z_v}/$zlib_lib"
make
make check-s 2>&1 | tee hdf5.test
make install
mv hdf5.test $ID/hdf5/${h_v}/
cd ../../
rm -rf hdf5-${h_v}
rm hdf5-${h_v}.tar.gz
echo "Completed installing hdf5"
[ -d $ID/hdf5/${h_v}/lib64 ] && hdf5_lib=lib64 || hdf5_lib=lib

####################
# Install NetCDF-C #
####################
tar xfz netcdf-${nc_v}.tar.gz
cd netcdf-${nc_v}
mkdir build ; cd build
../configure --prefix=$ID/netcdf/${nc_v} \
	--enable-shared --enable-static \
	--enable-netcdf-4 --disable-dap \
	CPPFLAGS="-I$ID/hdf5/${h_v}/include -I$ID/zlib/${z_v}/include" \
	LDFLAGS="-L$ID/hdf5/${h_v}/$hdf5_lib -Wl,-rpath=$ID/hdf5/${h_v}/$hdf5_lib \
	-L$ID/zlib/${z_v}/$zlib_lib -Wl,-rpath=$ID/zlib/${z_v}/$zlib_lib"
make
make install
cd ../../
rm -rf netcdf-${nc_v}
rm netcdf-${nc_v}.tar.gz
echo "Completed installing C NetCDF library"
[ -d $ID/netcdf/${nc_v}/lib64 ] && cdf_lib=lib64 || cdf_lib=lib

##########################
# Install NetCDF-Fortran #
##########################
tar xfz netcdf-fortran-${nf_v}.tar.gz
cd netcdf-fortran-${nf_v}
mkdir build ; cd build
../configure CPPFLAGS="-DgFortran -I$ID/zlib/${z_v}/include \
	-I$ID/hdf5/${h_v}/include -I$ID/netcdf/${nc_v}/include" \
	LIBS="-L$ID/zlib/${z_v}/$zlib_lib -Wl,-rpath=$ID/zlib/${z_v}/$zlib_lib \
	-L$ID/hdf5/${h_v}/$hdf5_lib -Wl,-rpath=$ID/hdf5/${h_v}/$hdf5_lib \
	-L$ID/netcdf/${nc_v}/$cdf_lib -Wl,-rpath=$ID/netcdf/${nc_v}/$cdf_lib \
	-lnetcdf -lhdf5hl_fortran -lhdf5_fortran -lhdf5_hl -lhdf5 -lz" \
	--prefix=$ID/netcdf/${nc_v} FC=gfortran --enable-static --enable-shared
make
make check 2>&1 | tee check.serial
make install
mv check.serial $ID/netcdf/${nc_v}/
cd ../../
rm -rf netcdf-fortran-${nf_v}
netcdf-fortran-${nf_v}.tar.gz
echo "Completed installing Fortran NetCDF library"

##########################
# Completed installation #
##########################

echo ""
echo ""
echo "##########################"
echo "# Completed installation #"
echo "#   of NetCDF package    #"
echo "#  and its dependencies  #"
echo "##########################"
echo ""
echo ""
########### END COPY ############

