%define build_java	1
%{?_with_java: %{expand: %%global build_java 1}}

%define name		vtk
%define version		5.2.1
%define vtkdir		%{_datadir}/%{name}

%define libname		%mklibname %{name}
%define libname_devel	%mklibname %{name} -d

%define bioxd_version	0.20090311
%define short_version	%(echo %{version} | cut -d. -f1,2)

%define vtkbindir	%{vtkdir}/bin
%define vtklibdir	%{_libdir}/%{name}-%{short_version}
%define vtkincdir	%{_includedir}/%{name}-%{short_version}
%define vtktcldir	%{tcl_sitearch}/%{name}-%{short_version}

%define qt_designer_plugins_dir	%{qt4plugins}/designer

Summary:	Toolkit for 3D computer graphics, image processing, and visualization
Name:		%{name}
Version:	%{version}
Release:	%{mkrel 1}
License:	BSD
Group:		Graphics
URL:		http://www.vtk.org/
Source0:	http://www.vtk.org/files/release/5.2/vtk-%{version}.tar.gz
Source1:	http://www.vtk.org/files/release/5.2/vtkdata-%{version}.tar.gz

# BioImageXD contains classes to read lsm files (from zeiss)
#URL:		http://www.bioimagexd.net
# svn co https://bioimagexd.svn.sourceforge.net/svnroot/bioimagexd/bioimagexd/trunk BioImageXD
# cd BioImageXD
# rm -fr `find . -type d -name .svn`
# rm -f bin/ffmpeg.exe bin/ffmpeg.osx bin/*.bat bin/*.dll bin/*.manifest bin/*.iss
# tar jcvf BioImageXD-0.`date +%\Y%\m%\d`.tar.bz2 BioImageXD
Source2:	BioImageXD-%{bioxd_version}.tar.bz2

# fix qt method calls in python
Patch0:		vtk-5.2.1-python-qt.patch
Patch1:		vtk-5.2.1-vtkLoadPythonTkWidgets.patch
Patch2:		vtk-5.2.1-tcl8.6.patch
Patch3:		vtk-5.2.1-fix-underlink.patch
Patch4:		vtk-5.2.1-Wformat=error.patch

# do not install widgets
Patch8:		vtk-BioImageXD-0.20090311-widgets.patch

BuildRoot:	%{_tmppath}/%{name}-root

BuildRequires:	cmake >= 1.8 
BuildRequires:	python-devel
BuildRequires:	X11-devel
BuildRequires:	expat-devel >= 2.0.1
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	tiff-devel
BuildRequires:	zlib-devel
BuildRequires:	freetype2-devel
BuildRequires:	perl
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	cvs
BuildRequires:	gnuplot
BuildRequires:	qt4-devel
BuildRequires:	tk-devel >= 8.6
BuildRequires:	tcl-devel >= 8.6
%if %{build_java}
BuildRequires:	java-rpmbuild
BuildRequires:	java-devel > 1.5
Requires:	java > 1.5
%endif

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

%if %{build_java}
%else
NOTE: The java wrapper is not included by default.  You may rebuild the srpm
      using "--with java" with JDK installed.
%endif

NOTE: This package is built with extra classes from the BioImageXD. Keep
      in mind that those classes are not part of the official CTK distribution
      and may change or be removed in the future.

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

%if %{build_java}
%else
NOTE: The java wrapper is not included by default.  You may rebuild the srpm
      using "--with java" with JDK installed.
%endif

%package -n %{libname_devel}
Summary:	VTK header files for building C++ code
Requires:	%{libname} = %{version}
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel < %{version}-%{release}
Conflicts:	%{libname}-qt < 5.0.3-4

%description -n %{libname_devel}
This provides the VTK header files required to compile C++
programs that use VTK to do 3D visualisation.

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

%package -n %{libname}-qt
Summary:	QT VTK widget
Requires:	vtk
Group:		System/Libraries

%description -n %{libname}-qt
The vtkQt classes combine VTK and Qt(TM) for X11.

%if %{build_java}
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
%endif

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

%package test-suite
Summary:	Tests programs for VTK
Requires:	%{libname} = %{version}
Requires:	%{name}-data = %{version}
Group:		Development/Other

%description test-suite
This package contains all testing programs from the VTK
source. The source code of these programs can be found in the
vtk-examples package.

%package doc
Summary:	Documentation for VTK
Group:		Development/Other
Obsoletes:	%{name}-docs < %{version}-%{release}
Provides:	%{name}-docs = %{version}-%{release}

%description doc
This package contains class APIs generated with doxygen.

%prep
%setup -q -n VTK

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# fix data path
find . -type f | xargs sed -i -e 's|../../../../VTKData|%{vtkdir}|g'

# install extra classes from BioImageXD
tar xf %{SOURCE2}
pushd BioImageXD
%patch8
sh bin/install_classes.sh . ..
popd

%if %{build_java}
export JAVA_HOME=%{java_home}
%endif

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
%cmake \
	-DCMAKE_SKIP_RPATH:BOOL=ON \
	-DVTK_DATA_ROOT:PATH=%{vtkdir} \
	-DVTK_WRAP_PYTHON:BOOL=ON \
%if %{build_java}
	-DJAVA_INCLUDE_PATH:PATH=$JAVA_HOME/include \
	-DJAVA_INCLUDE_PATH2:PATH=$JAVA_HOME/include/linux \
	-DJAVA_AWT_INCLUDE_PATH:PATH=$JAVA_HOME/include \
	-DVTK_WRAP_JAVA:BOOL=ON \
%else
	-DVTK_WRAP_JAVA:BOOL=OFF \
%endif
	-DVTK_WRAP_TCL:BOOL=ON \
	-DVTK_USE_RENDERING:BOOL=ON \
	-DDESIRED_QT_VERSION=4 \
	-DBUILD_DOCUMENTATION:BOOL=ON \
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
	-DVTK_BUILD_PREFIX=%{_prefix}

%make
# build docs
pushd Utilities/Doxygen
    make DoxygenDoc
popd

%install
rm -rf %{buildroot}
# drop "owner cannot overwrite file" default attributes
chmod u+w -R .
make install DESTDIR=%{buildroot} -C build

install -d -m 755 %{buildroot}%{vtkdir}
pushd %{buildroot}%{vtkdir}
    tar zxf %{SOURCE1}
    mv VTKData/{Baseline,Data} .
    rm -fr VTKData
popd

#install doc
install -d -m 755 %{buildroot}%{_docdir}/%{name}
cp -a build/Utilities/Doxygen/doc/html %{buildroot}%{_docdir}/%{name}/api

#install test-suite and examples
for d in Common Filtering Graphics Hybrid IO Imaging Parallel Rendering VolumeRendering Widgets
do
	mkdir -p %{buildroot}%{vtkdir}/examples/Testing/$d
	cp -a $d/Testing/* %{buildroot}%{vtkdir}/examples/Testing/$d
done
cp -a Examples %{buildroot}%{vtkdir}/examples

# get rid of unwanted files
pushd %{buildroot}%{vtkdir}/examples
  rm -f `find . -type d -name CVS`
  find . -name "*.o" -o -name "CMake*" -o -name "cmake.*"	\
	-o -name .NoDartCoverage -o -name .NoDartCoverage	\
	-o -name Makefile					\
	-exec rm {} \;
popd

# install test suite binaries and add each prg path in test-suite-files
rm -f test-suite-files
mkdir -p %{buildroot}%{vtkbindir}
pushd build/bin
    for f in `find . -type f | grep -v '.so$' | grep -v vtk`; do
	install -m 0755 $f %{buildroot}%{vtkbindir}
    done
popd
rm -f %{buildroot}%{vtkbindir}/*.so.*
%multiarch_includes  %{buildroot}%{vtkincdir}/vtkConfigure.h
%multiarch_includes  %{buildroot}%{vtkincdir}//vtknetcdf/ncconfig.h

# move test tcl files to the tcl location
mkdir -p %{buildroot}%{vtktcldir}/testing
mv -f %{buildroot}%{vtklibdir}/testing/*.tcl %{buildroot}%{vtktcldir}/testing

# drop files which which shouldn't be there
rm -rf %{buildroot}/TclTk
rm -rf %{buildroot}%{vtklibdir}/doc
mv -f %{buildroot}%{vtklibdir}/tcl/* %{buildroot}%{vtktcldir}

# install binaries in vtkdir
mv -f %{buildroot}%{_bindir}/* %{buildroot}%{vtkbindir}
# add some useful links
ln -sf %{vtkbindir}/%{name} %{buildroot}%{_bindir}/%{name}
ln -sf %{vtkbindir}/vtkpython %{buildroot}%{_bindir}/vtkpython
ln -sf %{_docdir}/%{name} %{buildroot}%{vtkdir}/doc

cp -fa README.html vtkLogo.jpg Copyright.txt Utilities/Upgrading %{buildroot}%{_docdir}/%{name}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n tcl-%{name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n python-%{name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libname}-qt -p /sbin/ldconfig
%endif

%if %{build_java}
%if %mdkversion < 200900
%post -n java-%{name} -p /sbin/ldconfig
%endif
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n tcl-%{name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n python-%{name} -p /sbin/ldconfig 
%endif

%if %mdkversion < 200900
%postun -n %{libname}-qt -p /sbin/ldconfig
%endif

%if %{build_java}
%if %mdkversion < 200900
%postun -n java-%{name} -p /sbin/ldconfig
%endif

%endif

%files -n %{libname}
%defattr(0755,root,root,0755)
%{vtklibdir}/lib*.so.*
%exclude %{vtklibdir}/libvtk*TCL*.so.*
%exclude %{vtklibdir}/libvtk*Python*.so.*
%exclude %{vtklibdir}/libQVTK.so.*
%exclude %{vtklibdir}/libvtk*Java.so.*

%files -n %{libname_devel}
%defattr(0644,root,root,0755)
%{_includedir}/*
%dir %{vtklibdir}
%{vtklibdir}/*.cmake
%{vtklibdir}/CMake
%{vtklibdir}/doxygen
%{vtklibdir}/hints
%{vtklibdir}/lib*.so
%exclude %{vtklibdir}/libvtk*TCL*.so
%exclude %{vtklibdir}/libvtk*Python*.so
%exclude %{vtklibdir}/libvtk*Java.so

%files test-suite
%defattr(0755,root,root,0755)
%{vtkbindir}/AmbientSpheres
%{vtkbindir}/Arrays
%{vtkbindir}/CommonCxxTests
%{vtkbindir}/Cone
%{vtkbindir}/Cone2
%{vtkbindir}/Cone3
%{vtkbindir}/Cone4
%{vtkbindir}/Cone5
%{vtkbindir}/Cone6
%{vtkbindir}/Cube
%{vtkbindir}/Cylinder
%{vtkbindir}/DiffuseSpheres
%{vtkbindir}/FilteringCxxTests
%{vtkbindir}/GenericFilteringCxxTests
%{vtkbindir}/GraphicsCxxTests
%{vtkbindir}/HierarchicalBoxPipeline
%{vtkbindir}/IOCxxTests
%{vtkbindir}/ImagingCxxTests
%{vtkbindir}/Medical1
%{vtkbindir}/Medical2
%{vtkbindir}/Medical3
%{vtkbindir}/MultiBlock
%{vtkbindir}/RGrid
%{vtkbindir}/RenderingCxxTests
%{vtkbindir}/SGrid
%{vtkbindir}/SocketClient
%{vtkbindir}/SocketServer
%{vtkbindir}/SpecularSpheres
%{vtkbindir}/TestCxxFeatures
%{vtkbindir}/TestInstantiator
%{vtkbindir}/VTKBenchMark
%{vtkbindir}/VolumeRenderingCxxTests
%{vtkbindir}/WidgetsCxxTests
%{vtkbindir}/finance
%{vtkbindir}/CreateTree
%{vtkbindir}/Example1
%{vtkbindir}/Example2
%{vtkbindir}/HelloWorld
%{vtkbindir}/HybridCxxTests
%{vtkbindir}/ImageSlicing
%{vtkbindir}/InfovisCxxTests
%{vtkbindir}/MaterialObjects
%{vtkbindir}/MultiView
%{vtkbindir}/ParallelCxxTests
%{vtkbindir}/ProcessShader
%{vtkbindir}/ProcessShader-real
%{vtkbindir}/QVTKCxxTests
%{vtkbindir}/TestFBOImplementation
%{vtkbindir}/Theme
%{vtkbindir}/TimeRenderer
%{vtkbindir}/TimeRenderer2
%{vtkbindir}/TreeLayout
%{vtkbindir}/ViewsCxxTests

%files -n tcl-%{name}
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{vtkbindir}/%{name}
%attr(0755,root,root) %{vtklibdir}/libvtk*TCL*.so.* 
%{vtktcldir}
%{_bindir}/%{name}

%files -n tcl-%{name}-devel
%defattr(0755,root,root,0755)
%{vtkbindir}/vtkWrapTcl
%{vtkbindir}/vtkWrapTclInit
%{vtklibdir}/*.tcl
%attr(0755,root,root) %{vtklibdir}/libvtk*TCL*.so 

%files -n python-%{name}
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{vtkbindir}/vtkpython
%attr(0755,root,root) %{vtklibdir}/libvtk*Python*.so.*
%dir %{vtklibdir}/testing
%{vtklibdir}/testing/*.py
%{python_sitelib}/vtk
%{python_sitelib}/VTK-*.egg-info
%{_bindir}/vtkpython

%files -n python-%{name}-devel
%defattr(0755,root,root,0755)
%{vtkbindir}/vtkWrapPython
%{vtkbindir}/vtkWrapPythonInit
%{vtklibdir}/libvtk*Python*.so

%files -n %{libname}-qt
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{vtkbindir}/qtevents
%attr(0755,root,root) %{vtkbindir}/qtimageviewer
%attr(0755,root,root) %{vtkbindir}/qtsimpleview
%attr(0755,root,root) %{vtklibdir}/libQVTK.so.*
%attr(0755,root,root) %{qt_designer_plugins_dir}/libQVTKWidgetPlugin.so

%if %{build_java}
%files -n java-%{name}
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{vtkbindir}/vtkParseJava
%attr(0755,root,root) %{vtkbindir}/vtkWrapJava
%attr(0755,root,root) %{vtkbindir}/VTKJavaExecutable
%attr(0755,root,root) %{vtklibdir}/libvtk*Java.so*
%{vtklibdir}/java
%endif

%files		examples
%defattr(0644,root,root,0755)
%dir %{vtkdir}/examples
%{vtkdir}/examples/*

%files		doc
%defattr(0644,root,root,0755)
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/*

%files		data
%defattr(-,root,root)
%{vtkdir}/*

%clean 
rm -rf %{buildroot}
