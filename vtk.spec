# Documentation are download and built by vtk-doc separated package
%bcond_with java

%define libname		%mklibname %{name}
%define libname_devel	%mklibname %{name} -d

%define bioxd_version	0.20090311
%define short_version	%(echo %{version} | cut -d. -f1,2)

%define vtkincdir	%_includedir/vtk
%define vtkdocdir	%_docdir/vtk
%define vtktcldir	%{tcl_sitearch}/%{name}-%{short_version}

%define qt_designer_plugins_dir	%{qt4plugins}/designer

Name: vtk
Version: 5.4.2
Release: %mkrel 6
Summary: Toolkit for 3D computer graphics, image processing, and visualization
License: BSD
Group: Graphics
URL: http://www.vtk.org/
Source0: http://www.vtk.org/files/release/5.2/vtk-%{version}.tar.gz
Source1: http://www.vtk.org/files/release/5.2/vtkdata-%{version}.tar.gz

# BioImageXD contains classes to read lsm files (from zeiss)
#URL:		http://www.bioimagexd.net
# svn co https://bioimagexd.svn.sourceforge.net/svnroot/bioimagexd/bioimagexd/trunk BioImageXD
# cd BioImageXD
# rm -fr `find . -type d -name .svn`
# rm -f bin/ffmpeg.exe bin/ffmpeg.osx bin/*.bat bin/*.dll bin/*.manifest bin/*.iss
# tar jcvf BioImageXD-0.`date +%\Y%\m%\d`.tar.bz2 BioImageXD
Source2:	BioImageXD-%{bioxd_version}.tar.bz2

# fix qt method calls in python
Patch0:	vtk-5.2.1-python-qt.patch
Patch1:	vtk-5.2.1-vtkLoadPythonTkWidgets.patch
Patch2:	vtk-5.2.1-tcl8.6.patch
Patch3:	vtk-5.2.1-fix-underlink.patch

# do not install widgets
Patch8:		vtk-BioImageXD-0.20090311-widgets.patch

BuildRoot:	%{_tmppath}/%{name}-root

BuildRequires:	cmake >= 1.8 
BuildRequires:	X11-devel
BuildRequires:	expat-devel >= 2.0.1
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	tiff-devel
BuildRequires:	zlib-devel
BuildRequires:	freetype2-devel
BuildRequires:	GL-devel
BuildRequires:	perl
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	cvs
BuildRequires:	gnuplot
BuildRequires:	qt4-devel
BuildRequires:	tk-devel >= 8.6
BuildRequires:	tcl-devel >= 8.6
BuildRequires:  libxml2-devel
BuildRequires:  boost-devel
BuildRequires:  libopenssl-devel
BuildRequires:  python
%if %with java
BuildRequires:	java-rpmbuild
BuildRequires:	java-devel > 1.5
%endif
%py_requires -d

%description
The Visualization ToolKit (VTK) is an object oriented software system for 3D
computer graphics, image processing, and visualization. VTK includes a
textbook, a C++ class library, and several interpreted interface layers
including Tcl/Tk, Java, and Python. VTK supports a wide variety of
visualization algorithms including scalar, vector, tensor, texture, and
volumetric methods. It also supports advanced modeling techniques like
implicit modeling, polygon reduction, mesh smoothing, cutting, contouring,
and Delaunay triangulation.  Moreover, dozens of imaging algorithms have been
integrated into the system. This allows mixing 2D imaging / 3D graphics
algorithms and data.

%if ! %with java
NOTE: The java wrapper is not included by default.  You may rebuild the srpm
      using "--with java" with JDK installed.
%endif

NOTE: This package is built with extra classes from the BioImageXD. Keep
      in mind that those classes are not part of the official CTK distribution
      and may change or be removed in the future.

#------------------------------------------------------------------------------

%package -n %{libname}
Summary:	Toolkit for 3D computer graphics, image processing, and visualization
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name} < %{version}-%{release}

%description -n %{libname}
The Visualization ToolKit (VTK) is an object oriented software system for 3D
computer graphics, image processing, and visualization. VTK includes a
textbook, a C++ class library, and several interpreted interface layers
including Tcl/Tk, Java, and Python. VTK supports a wide variety of
visualization algorithms including scalar, vector, tensor, texture, and
volumetric methods. It also supports advanced modeling techniques like
implicit modeling, polygon reduction, mesh smoothing, cutting, contouring,
and Delaunay triangulation.  Moreover, dozens of imaging algorithms have been
integrated into the system. This allows mixing 2D imaging / 3D graphics
algorithms and data.

%if ! %with java
NOTE: The java wrapper is not included by default.  You may rebuild the srpm
      using "--with java" with JDK installed.
%endif

%files -n %{libname}
%defattr(0755,root,root,0755)
%_libdir/lib*.so.*
%exclude %_libdir/libvtk*TCL*.so.*
%exclude %_libdir/libvtk*Python*.so.*
%exclude %_libdir/libQVTK.so.*
%exclude %_libdir/libvtkQtChart.so.*
%if %with java
%exclude %_libdir/libvtk*Java.so.*
%endif

#------------------------------------------------------------------------------

%package -n %{libname_devel}
Summary:	VTK header files for building C++ code
Requires:	%{libname} = %{version}
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel < %{version}-%{release}
Conflicts:	%{libname}-qt < 5.0.3-4
Requires:	%{libname}-qt = %{version}-%{release}

%description -n %{libname_devel}
This provides the VTK header files required to compile C++
programs that use VTK to do 3D visualisation.

%files -n %{libname_devel}
%defattr(0644,root,root,0755)
%{_includedir}/*
%dir %_libdir
%dir %_libdir/vtk/
%_libdir/vtk/*
%_libdir/lib*.so
%exclude %_libdir/libvtk*TCL*.so
%exclude %_libdir/libvtk*Python*.so
%if %with java
%exclude %_libdir/libvtk*Java.so
%endif



#------------------------------------------------------------------------------

%package -n tcl-%{name}
Summary:	Tcl bindings for VTK
Group:		Development/Other
Requires:	%{libname} = %{version}
Obsoletes:	%{name}-tcl
Provides:	%{name}-tcl

%description -n tcl-%{name}
The Visualization ToolKit (VTK) is an object oriented software system for 3D
computer graphics, image processing, and visualization. VTK includes a
textbook, a C++ class library, and several interpreted interface layers
including Tcl/Tk, Java, and Python. VTK supports a wide variety of
visualization algorithms including scalar, vector, tensor, texture, and
volumetric methods. It also supports advanced modeling techniques like
implicit modeling, polygon reduction, mesh smoothing, cutting, contouring,
and Delaunay triangulation.  Moreover, dozens of imaging algorithms have been
integrated into the system. This allows mixing 2D imaging / 3D graphics
algorithms and data.

This package contains tcl bindings for VTK.

%files -n tcl-%{name}
%defattr(0644,root,root,0755)
%attr(0755,root,root) %_bindir/%{name}
%attr(0755,root,root) %_libdir/libvtk*TCL*.so.* 
%_libdir/vtk/testing/*.tcl
%_libdir/tcl
%{vtktcldir}

#------------------------------------------------------------------------------

%package -n tcl-%{name}-devel
Summary:	Tcl bindings for VTK
Group:		Development/Other
Requires:	tcl-%{name} = %{version}

%description -n tcl-%{name}-devel
The Visualization ToolKit (VTK) is an object oriented software system for 3D
computer graphics, image processing, and visualization. VTK includes a
textbook, a C++ class library, and several interpreted interface layers
including Tcl/Tk, Java, and Python. VTK supports a wide variety of
visualization algorithms including scalar, vector, tensor, texture, and
volumetric methods. It also supports advanced modeling techniques like
implicit modeling, polygon reduction, mesh smoothing, cutting, contouring,
and Delaunay triangulation.  Moreover, dozens of imaging algorithms have been
integrated into the system. This allows mixing 2D imaging / 3D graphics
algorithms and data.
 
This package contains tcl bindings for VTK.

%files -n tcl-%{name}-devel
%defattr(0755,root,root,0755)
%_bindir/vtkWrapTcl
%_bindir/vtkWrapTclInit
%_libdir/*.tcl
%attr(0755,root,root) %_libdir/libvtk*TCL*.so 

#------------------------------------------------------------------------------

%package -n python-%{name}
Summary:	Python bindings for VTK
Requires:	%{libname} = %{version}
Requires(pre):	%{libname} = %{version}
Group:		Development/Python
Obsoletes:	%{name}-python
Provides:	%{name}-python

%description -n python-%{name} 
The Visualization ToolKit (VTK) is an object oriented software system for 3D
computer graphics, image processing, and visualization. VTK includes a
textbook, a C++ class library, and several interpreted interface layers
including Tcl/Tk, Java, and Python. VTK supports a wide variety of
visualization algorithms including scalar, vector, tensor, texture, and
volumetric methods. It also supports advanced modeling techniques like
implicit modeling, polygon reduction, mesh smoothing, cutting, contouring,
and Delaunay triangulation.  Moreover, dozens of imaging algorithms have been
integrated into the system. This allows mixing 2D imaging / 3D graphics
algorithms and data.

This package contains python bindings for VTK.

%files -n python-%{name}
%defattr(0644,root,root,0755)
%_bindir/vtkpython
%_libdir/libvtk*Python*.so.*
%_libdir/vtk/testing/*.py
%{python_sitelib}/vtk
%{python_sitelib}/VTK-*.egg-info

#------------------------------------------------------------------------------

%package -n python-%{name}-devel
Summary:	Python bindings for VTK
Requires:	python-%{name} = %{version}
Group:		Development/Python

%description -n python-%{name}-devel
The Visualization ToolKit (VTK) is an object oriented software system for 3D
computer graphics, image processing, and visualization. VTK includes a
textbook, a C++ class library, and several interpreted interface layers
including Tcl/Tk, Java, and Python. VTK supports a wide variety of
visualization algorithms including scalar, vector, tensor, texture, and
volumetric methods. It also supports advanced modeling techniques like
implicit modeling, polygon reduction, mesh smoothing, cutting, contouring,
and Delaunay triangulation.  Moreover, dozens of imaging algorithms have been
integrated into the system. This allows mixing 2D imaging / 3D graphics
algorithms and data.

This package contains python bindings for VTK.

%files -n python-%{name}-devel
%defattr(0755,root,root,0755)
%_bindir/vtkWrapPython
%_bindir/vtkWrapPythonInit
%_libdir/libvtk*Python*.so

#------------------------------------------------------------------------------

%package -n %{libname}-qt
Summary:	QT VTK widget
Requires:	vtk
Group:		System/Libraries

%description -n %{libname}-qt
The vtkQt classes combine VTK and Qt(TM) for X11.

%files -n %{libname}-qt
%defattr(0644,root,root,0755)
%_bindir/qtevents
%_bindir/qtimageviewer
%_bindir/qtsimpleview
%_libdir/libQVTK.so.*
%_libdir/libvtkQtChart.so.*
%{qt_designer_plugins_dir}/libQVTKWidgetPlugin.so

#------------------------------------------------------------------------------

%if %with java
%package -n java-%{name}
Summary:	Java bindings for VTK
Group:		Development/Java
Requires:	%{libname} = %{version}
Obsoletes:	%{name}-java
Provides:	%{name}-java

%description -n java-%{name}
The Visualization ToolKit (VTK) is an object oriented software system for 3D
computer graphics, image processing, and visualization. VTK includes a
textbook, a C++ class library, and several interpreted interface layers
including Tcl/Tk, Java, and Python. VTK supports a wide variety of
visualization algorithms including scalar, vector, tensor, texture, and
volumetric methods. It also supports advanced modeling techniques like
implicit modeling, polygon reduction, mesh smoothing, cutting, contouring,
and Delaunay triangulation.  Moreover, dozens of imaging algorithms have been
integrated into the system. This allows mixing 2D imaging / 3D graphics
algorithms and data.

This package contains Java bindings for VTK.

%files -n java-%{name}
%defattr(0644,root,root,0755)
%_bindir/vtkParseJava
%_bindir/vtkWrapJava
%_bindir/VTKJavaExecutable
%_libdir/libvtk*Java.so*
%_libdir/java

%endif

#------------------------------------------------------------------------------

%package	data
Summary:	Data and Baseline images for VTK regression testing
Group:		Development/Other

%description	data
Data and Baseline images for VTK regression testing and other VTK examples.

The VTKData/Data directory are data files of various types. This includes
polygonal data, images, volumes, structured grids, rectilinear grids,
and multi-variate data.

The VTKData/Baseline are the testing images. These are used in testing to
compare a valid image against a generated image. If a difference between
the two images is found, then the test is considered to have failed.

%files		data
%defattr(-,root,root)
%_datadir/vtk

#------------------------------------------------------------------------------

%package examples
Summary:	C++, Tcl and Python example programs/scripts for VTK
Group:		Development/Other
Requires:	%{name}-data = %{version}
Requires:	%{libname} = %{version}

%description examples
This package contains all the examples from the VTK source.
To compile the C++ examples you will need to install the vtk-devel
package as well. The Python and Tcl examples can be run with the
corresponding packages (vtk-python, vtk-tcl).

%files		examples
%defattr(0644,root,root,0755)
%dir %{vtkdocdir}/examples
%{vtkdocdir}/examples/*

#------------------------------------------------------------------------------

%package test-suite
Summary:	Tests programs for VTK
Requires:	%{libname} = %{version}
Requires:	%{name}-data = %{version}
Group:		Development/Other

%description test-suite
This package contains all testing programs from the VTK
source. The source code of these programs can be found in the
vtk-examples package.

%files test-suite
%defattr(0755,root,root,0755)
%_bindir/*
%exclude %_bindir/%{name}
%exclude %_bindir/vtkWrapTcl
%exclude %_bindir/vtkWrapTclInit

#------------------------------------------------------------------------------

%prep
%setup -q -n VTK

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# fix data path
find . -type f | xargs sed -i -e 's|../../../../VTKData|%_datadir/vtk|g'

# install extra classes from BioImageXD
tar xf %{SOURCE2}
pushd BioImageXD
%patch8
sh bin/install_classes.sh . ..
popd

for f in  {vtkImageAutoThresholdColocalization,vtkIntensityTransferFunction}.{cxx,h}; do
    ln -sf ../BioImageXD/vtkBXD/Processing/$f Filtering
done
ln -sf ../BioImageXD/vtkBXD/Processing/vtkBXDProcessingWin32Header.h Filtering
sed -e 's|cmakedefine|define|' BioImageXD/vtkBXD/VTKBXDConfigure.h.in > Filtering/VTKBXDConfigure.h

for f in  {vtkImageLabelAverage,vtkImageSolitaryFilter,vtkImageSimpleMIP,vtkImageMapToIntensities,vtkImageColocalizationTest,vtkImageColocalizationFilter,vtkImageAlphaFilter,vtkImageColorMerge}.{cxx,h}; do
    ln -sf ../BioImageXD/vtkBXD/Processing/$f Imaging
done

for f in  {vtkLSMReader,vtkExtTIFFReader}.{cxx,h}; do
    ln -sf ../BioImageXD/vtkBXD/Processing/$f IO
done

%build

# Remove old cmake files
rm -f CMake/FindBoost*

# Due to cmake prefix point already for _prefix, we need
# push only the necessary extra paths

%cmake \
	-DVTK_INSTALL_LIB_DIR=/%_lib \
	-DVTK_INSTALL_BIN_DIR=/bin \
	-DVTK_INSTALL_PACKAGE_DIR=/%_lib/vtk \
	-DVTK_INSTALL_INCLUDE_DIR=/include/vtk \
	-DVTK_DATA_ROOT=/share/vtk \
	-DVTK_USE_SYSTEM_LIBPROJ4:BOOL=OFF \
	-DVTK_WRAP_PYTHON:BOOL=ON \
%if %with java
	-DJAVA_INCLUDE_PATH:PATH=%{java_home}/include \
	-DJAVA_INCLUDE_PATH2:PATH=%{java_home}/include/linux \
	-DJAVA_AWT_INCLUDE_PATH:PATH=%{java_home}/include \
	-DVTK_WRAP_JAVA:BOOL=ON \
%else
	-DVTK_WRAP_JAVA:BOOL=OFF \
%endif
	-DVTK_WRAP_TCL:BOOL=ON \
	-DVTK_USE_RENDERING:BOOL=ON \
	-DDESIRED_QT_VERSION=4 \
	-DBUILD_DOCUMENTATION:BOOL=OFF \
	-DBUILD_EXAMPLES:BOOL=ON \
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DBUILD_TESTING:BOOL=ON \
	-DVTK_USE_SYSTEM_EXPAT:BOOL=ON \
	-DVTK_USE_SYSTEM_JPEG:BOOL=ON \
	-DVTK_USE_SYSTEM_PNG:BOOL=ON \
	-DVTK_USE_SYSTEM_TIFF:BOOL=ON \
	-DVTK_USE_SYSTEM_ZLIB:BOOL=ON \
	-DVTK_USE_SYSTEM_FREETYPE:BOOL=ON \
	-DVTK_USE_ANSI_STDLIB:BOOL=ON \
	-DVTK_USE_PARALLEL:BOOL=ON \
	-DVTK_USE_GUISUPPORT:BOOL=ON \
	-DVTK_USE_QVTK:BOOL=ON \
	-DVTK_PYTHON_SETUP_ARGS:STRING="--prefix=%{_prefix} --root=%{buildroot}" \
	-DVTK_INSTALL_QT_PLUGIN_DIR:STRING=%{qt_designer_plugins_dir} \
	-DVTK_USE_GL2PS:BOOL=ON	\
	-DVTK_HAVE_GETSOCKNAME_WITH_SOCKLEN_T:INTERNAL=1 \
	-DVTK_USE_SYSTEM_LIBXML2:BOOL=ON \
	-DVTK_USE_QVTK_QTOPENGL:BOOL=ON \
	-DVTK_USE_BOOST:BOOL=ON 

%make

%install
rm -rf %{buildroot}
%makeinstall_std -C build

mkdir -p %{buildroot}%{vtktcldir}

install -d -m 755 %{buildroot}/%_datadir/vtk
pushd %{buildroot}/%_datadir/vtk
    tar zxf %{SOURCE1}
    mv VTKData/{Baseline,Data} .
    rm -fr VTKData
popd

#install test-suite and examples
for d in Common Filtering Graphics Hybrid IO Imaging Parallel Rendering VolumeRendering Widgets
do
	mkdir -p %{buildroot}%{vtkdocdir}/examples/Testing/$d
	cp -a $d/Testing/* %{buildroot}%{vtkdocdir}/examples/Testing/$d
done
cp -a Examples %{buildroot}%{vtkdocdir}/examples

# get rid of unwanted files
pushd %{buildroot}%{vtkdocdir}/examples
  rm -f `find . -type d -name CVS`
  find . -name "*.o" -o -name "CMake*" -o -name "cmake.*"	\
	-o -name .NoDartCoverage -o -name .NoDartCoverage	\
	-o -name Makefile					\
	-exec rm {} \;
popd
# Remove any possible verdict docs
rm -rf %buildroot/%_libdir/vtk/doc
rm -rf %buildroot/%{vtkdocdir}/verdict

# install test suite binaries and add each prg path in test-suite-files
rm -f test-suite-files
mkdir -p %{buildroot}%_bindir
pushd build/bin
    for f in `find . -type f | grep -v '.so$' | grep -v vtk`; do
	install -m 0755 $f %{buildroot}%_bindir
    done
popd
rm -f %buildroot%_bindir/*.so.*
%multiarch_includes  %{buildroot}%{vtkincdir}/vtkConfigure.h
%multiarch_includes  %{buildroot}%{vtkincdir}/vtknetcdf/ncconfig.h

%clean 
rm -rf %{buildroot}
