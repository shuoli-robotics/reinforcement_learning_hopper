# Scrit for the instalation of Ipopt
# https://www.coin-or.org/Ipopt/documentation/
# https://www.coin-or.org/Ipopt/documentation/node10.html

echo "Download legged software"
roscd;cd ../src
git clone https://RDaneelOlivaw@bitbucket.org/RDaneelOlivaw/loco_motion.git

echo "Donwload software for motions for legged robots"
echo "Install Stuff for TOWR"
sudo apt-get install libncurses5-dev libncursesw5-dev xterm ros-kinetic-desktop-full ros-kinetic-xpp
roscd;cd ../src
git clone https://github.com/ethz-adrl/towr.git

echo "Download ifopt solver packages"
roscd;cd ../src
git clone https://github.com/ethz-adrl/ifopt.git

echo "Check Compilation Tools"
sudo apt-get install gcc g++ gfortran subversion patch wget
echo "Getting the IPOPT code svn, tarball is broken"
cd
svn co https://projects.coin-or.org/svn/Ipopt/stable/3.12 CoinIpopt
cd CoinIpopt
IPOPTDIR=$(pwd)

echo "Get Third party libraries for the compilation of IPOPT"
cd $IPOPTDIR/ThirdParty/Blas 
./get.Blas 
cd ../Lapack 
./get.Lapack 
cd ../ASL 
./get.ASL
cd $IPOPTDIR

echo "Create a directory where you want to compile IPOPT, for example"
mkdir $IPOPTDIR/build
cd $IPOPTDIR/build
echo "Run the configure script"
$IPOPTDIR/configure
echo "Build the code"
make
# make test gives error if HSL is not install because they use the M27 models
#make test
echo "libs installed in CoinIpopt/build/lib"
make install

echo "NOT Install SNOPT, its also single user and license stuff."

echo "Edit path to the installed libraries in the CMakelists of the ifopt packages"
roscd legged_robots_sims/install_scripts
LEGGED_PKG_INSTALL_SCRIPTS=$(pwd)
roscd ifopt_ipopt
#Create temporary file with new line in place
ls $IPOPTDIR/build/include/coin
python $LEGGED_PKG_INSTALL_SCRIPTS/replace_text.py CMakeLists.txt "/home/winklera/3rd_party_software/Ipopt-3.12.8" $IPOPTDIR CMakeLists.txt
roscd ifopt_snopt
#Create temporary file with new line in place
# SNOPT is also by formulary 
#ls $IPOPTDIR/build/include/coin
#python $LEGGED_PKG_INSTALL_SCRIPTS/replace_text.py CMakeLists.txt "/home/winklera/3rd_party_software/snopt_lib" $IPOPTDIR/ CMakeLists.txt

echo "Compile Everything"
roscd;cd ..
rm -rf build/ devel/
catkin_make -DCMAKE_BUILD_TYPE=Release

catkin_make run_tests


