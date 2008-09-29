# TODO: - test the java build

%define build_java 0
%{?_with_java: %{expand: %%global build_java 1}}

%define name 	vtk
%define version 5.0.3
%define release %mkrel 4

%define short_version %(echo %{version} | cut -d. -f1,2)
%define libname %mklibname %{name}
%define libname_devel %mklibname %{name} -d

%define qt_designer_plugins_dir %{qt4plugins}/designer

Summary:   	Toolkit for 3D computer graphics, image processing, and visualization
Name:      	%name
Version:   	%version
Release:   	%release
License:   	BSD
Group:     	Graphics
Url:	   	http://public.kitware.com/VTK/
Source0:   	http://www.vtk.org/files/release/%{short_version}/vtk-%{version}.tar.bz2
# fix qt method calls in python
Patch0:		vtk-python-qt.patch
Patch1:		vtk-vtkLoadPythonTkWidgets.patch
# tcl 8.5 fix
Source10:	tk8.5.tar.bz2
Patch2:		vtk-tcl8.5.patch
# fixes for gcc 4.3
Patch3:		vtk-gcc4.3.patch
# support cmake's libsuffix
Patch4:		vtk-libsuffix.patch
Patch5:		vtk-fix-underlink.patch
Patch6:		vtk-python-2.5.patch
# BioImageXD contains classes to read lsm files (from zeiss)
Source1:	BioImageXD.tar.bz2
# do not install widgets
Patch10:        vtk-bioimagexd-widgets.patch
BuildRoot: 	%{_tmppath}/%name-root
BuildRequires: 	cmake >= 1.8 
BuildRequires:  python-devel
BuildRequires:  tcl
BuildRequires:  X11-devel
BuildRequires:  expat-devel >= 2.0.1
BuildRequires:  jpeg-devel
BuildRequires:  png-devel
BuildRequires:  tiff-devel
BuildRequires:  zlib-devel
BuildRequires:  freetype2-devel
BuildRequires:  perl
BuildRequires: 	doxygen
BuildRequires:  graphviz
BuildRequires:  cvs
BuildRequires:  gnuplot
BuildRequires:  tcl
BuildRequires:  tk
BuildRequires:  qt4-devel
# needed for backport to 2006.0
%if %mdkversion >= 200610
BuildRequires:	tk-devel
BuildRequires:	tcl-devel
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

NOTE: The java wrapper is not included by default.  You may rebuild the srpm
      using "--with java" with JDK installed.

NOTE: This package is built with extra classes from the BioImageXD. Keep
      in mind that those classes are not part of the official CTK distribution
      and may change or be removed in the future.

%package -n %libname
Summary:	Toolkit for 3D computer graphics, image processing, and visualization
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name}

%description -n %libname
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

NOTE: The java wrapper is not included by default.  You may rebuild the srpm
      using "--with java" with JDK installed.


%package -n %libname_devel
Summary:	VTK header files for building C++ code
Requires:	%{libname} = %{version}
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel
Conflicts:	%{libname}-qt < 5.0.3-4

%description -n %libname_devel
This provides the VTK header files required to compile C++
programs that use VTK to do 3D visualisation.

%package -n tcl-%{name}
Summary:  Tcl bindings for VTK
Group:    Development/Other
Requires: %{libname} = %{version}
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
Summary:  Tcl bindings for VTK
Group:    Development/Other
Requires: tcl-%{name} = %{version}

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
Summary: Python bindings for VTK
Requires: %{libname} = %{version}
Requires(pre): %{libname} = %{version}
Group:   Development/Python
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
Summary: Python bindings for VTK
Requires: python-%{name} = %{version}
Group:   Development/Python

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
Summary: QT VTK widget
Requires: vtk
Group: System/Libraries

%description -n %{libname}-qt
The vtkQt classes combine VTK and Qt(TM) for X11.

%if %build_java
%package -n java-%{name}
Summary: Java bindings for VTK
Group:   Development/Java
Requires: %{libname} = %{version}
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

This package contains java bindings for VTK.

%endif

%package examples
Summary:  C++, Tcl and Python example programs/scripts for VTK
Group:    Development/Other
Requires: %{name}-data = %{version}
Requires: %{libname} = %{version}

%description examples
This package contains all the examples from the VTK source.
To compile the C++ examples you will need to install the vtk-devel
package as well. The Python and Tcl examples can be run with the
corresponding packages (vtk-python, vtk-tcl).

%package test-suite
Summary:  Tests programs for VTK
Requires: %{libname} = %{version}
Requires: %{name}-data = %{version}
Group:    Development/Other

%description test-suite
This package contains all testing programs from the VTK
source. The source code of these programs can be found in the
vtk-examples package.

%package doc
Summary: Documentation for VTK
Group:   Development/Other
Obsoletes: %{name}-docs
Provides: %{name}-docs

%description doc
This package contains class api generated with doxygen.

%prep
%setup -q -n VTK
%patch0 -p1
%patch1 -p0
%patch3 -p1
%patch4 -p0
%patch5 -p0
%patch6 -p0

# fix for tcl 8.5
%patch2 -p1
cd Utilities/TclTk
tar xjf %{SOURCE10}
cd -

rm -rf `find -type d -name CVS`

# fix data path
find -type f | xargs perl -pi -e 's#../../../../VTKData#%{_datadir}/vtk-data#g'

# install extra classes from BioImageXD
tar xjf %{SOURCE1}
cd BioImageXD
rm -rf `find -type d -name .svn`
%patch10
sh bin/install_classes.sh . ..

%build
%define _disable_ld_as_needed 1
%cmake \
	-DCMAKE_SKIP_RPATH:BOOL=ON \
	-DVTK_DATA_ROOT:PATH=%{_datadir}/vtk-data-%{version} \
	-DVTK_WRAP_PYTHON:BOOL=ON \
	-DVTK_WRAP_JAVA:BOOL=OFF \
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

%if %build_java
cmake	-DJAVA_INCLUDE_PATH:PATH=$JAVA_HOME/include \
	-DJAVA_INCLUDE_PATH2:PATH=$JAVA_HOME/include/linux \
	-DJAVA_AWT_INCLUDE_PATH:PATH=$JAVA_HOME/include \
	-DJAVA_AWT_LIBRARY:PATH=$JAVA_HOME/jre/lib/i386/libawt.so \
	-DVTK_WRAP_JAVA:BOOL=ON \
.
%endif


#	-DCMAKE_BUILD_TYPE:STRING=Release \
# 	-DOPENGL_LIBRARY:FILEPATH=/usr/X11R6/lib/libGL.so.1.0
#	-DCMAKE_SKIP_RPATH:BOOL=ON \
#	-DLIBRARY_OUTPUT_PATH:PATH=$RPM_BUILD_DIR/VTK-%version/lib \
#	-DEXECUTABLE_OUTPUT_PATH:PATH=$RPM_BUILD_DIR/VTK-%version/bin \
# -Wno-deprecated -fpermissive 

%make
# build docs
(
cd Utilities/Doxygen
%make DoxygenDoc
)

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} -C build

%if %build_java
#install java
install -d -m 755 %{buildroot}%{_libdir}/vtk/java
install  -m 644 lib/vtk.jar     %{buildroot}%{_libdir}/vtk/java
install  -m 644 java/vtk/*.java %{buildroot}%{_libdir}/vtk/java
%endif

#install doc
install -d -m 755 %{buildroot}%{_datadir}/vtk-docs
cp -a build/Utilities/Doxygen/doc/html %{buildroot}%{_datadir}/vtk-docs/api

#install test-suite and examples
for d in Common Filtering Graphics Hybrid IO Imaging Parallel Rendering VolumeRendering Widgets
do
	mkdir -p %{buildroot}%{_datadir}/vtk-examples/Testing/$d
	cp -a $d/Testing/* %{buildroot}%{_datadir}/vtk-examples/Testing/$d
done
cp -a Examples %{buildroot}%{_datadir}/vtk-examples

# get rid of unwanted files
find %{buildroot}%{_datadir}/vtk-examples -name "*.o" -exec rm -f {} \;
find %{buildroot}%{_datadir}/vtk-examples -name CMakeCache.txt -exec rm -f {} \;
find %{buildroot}%{_datadir}/vtk-examples -name Makefile -exec rm -f {} \;
find %{buildroot}%{_datadir}/vtk-examples -name DartTestfile.txt -exec rm -f {} \;
find %{buildroot}%{_datadir}/vtk-examples -name .NoDartCoverage -exec rm -f {} \;
find %{buildroot}%{_datadir}/vtk-examples -name "cmake.*" -exec rm -f {} \;
rm -rf `find %{buildroot}%{_datadir}/vtk-examples -name CVS -type d`
rm -rf `find %{buildroot}%{_datadir}/vtk-examples -name "CMake*"`

# install test suite binaries and add each prg path in test-suite-files
rm -f %buildroot%_bindir/*.so.*
%multiarch_includes  %{buildroot}%{_includedir}/vtk-*/vtkConfigure.h
%multiarch_includes  %{buildroot}%{_includedir}/vtk-*/vtknetcdf/ncconfig.h

# drop files which which shouldn't be there
rm -rf %{buildroot}/TclTk

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

%if %build_java
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

%if %build_java
%if %mdkversion < 200900
%postun -n java-%{name} -p /sbin/ldconfig
%endif

%endif

%files -n %{libname}
%defattr(0755,root,root,0755)
%doc README.html vtkLogo.jpg Copyright.txt
%{_libdir}/libvtkCommon.so.*
%{_libdir}/libvtkDICOMParser.so.*
%{_libdir}/libvtkFiltering.so.*
%{_libdir}/libvtkGenericFiltering.so.*
%{_libdir}/libvtkGraphics.so.*
%{_libdir}/libvtkHybrid.so.*
%{_libdir}/libvtkImaging.so.*
%{_libdir}/libvtkIO.so.*
%{_libdir}/libvtkNetCDF.so.*
%{_libdir}/libvtkRendering.so.*
%{_libdir}/libvtkVolumeRendering.so.*
%{_libdir}/libvtkWidgets.so.*
%{_libdir}/libvtkexoIIc.so.*
%{_libdir}/libvtkftgl.so.*
%{_libdir}/libvtksys.so.*
%{_libdir}/libvtkParallel.so.*

%files -n %{libname_devel}
%defattr(0644,root,root,0755)
%{_includedir}/*
%dir %{_libdir}/vtk-*
%{_libdir}/vtk-*/*.cmake
%{_libdir}/vtk-*/CMake
%{_libdir}/vtk-*/doxygen
%{_libdir}/vtk-*/hints
%{_libdir}/libQVTK.so
%{_libdir}/libvtkCommon.so
%{_libdir}/libvtkDICOMParser.so
%{_libdir}/libvtkFiltering.so
%{_libdir}/libvtkGenericFiltering.so
%{_libdir}/libvtkGraphics.so
%{_libdir}/libvtkHybrid.so
%{_libdir}/libvtkImaging.so
%{_libdir}/libvtkIO.so
%{_libdir}/libvtkNetCDF.so
%{_libdir}/libvtkRendering.so
%{_libdir}/libvtkVolumeRendering.so
%{_libdir}/libvtkWidgets.so
%{_libdir}/libvtkexoIIc.so
%{_libdir}/libvtkftgl.so
%{_libdir}/libvtksys.so
%{_libdir}/libvtkParallel.so
%doc Utilities/Upgrading/*

%files test-suite
%defattr(0755,root,root,0755)
%{_bindir}/AmbientSpheres
%{_bindir}/Arrays
%{_bindir}/CommonCxxTests
%{_bindir}/Cone
%{_bindir}/Cone2
%{_bindir}/Cone3
%{_bindir}/Cone4
%{_bindir}/Cone5
%{_bindir}/Cone6
%{_bindir}/Cube
%{_bindir}/Cylinder
%{_bindir}/DiffuseSpheres
%{_bindir}/FilteringCxxTests
%{_bindir}/GenericFilteringCxxTests
%{_bindir}/GraphicsCxxTests
%{_bindir}/HierarchicalBoxPipeline
%{_bindir}/IOCxxTests
%{_bindir}/ImagingCxxTests
%{_bindir}/Medical1
%{_bindir}/Medical2
%{_bindir}/Medical3
%{_bindir}/MultiBlock
%{_bindir}/RGrid
%{_bindir}/RenderingCxxTests
%{_bindir}/SGrid
%{_bindir}/SocketClient
%{_bindir}/SocketServer
%{_bindir}/SpecularSpheres
%{_bindir}/TestCxxFeatures
%{_bindir}/TestInstantiator
%{_bindir}/VTKBenchMark
%{_bindir}/VolumeRenderingCxxTests
%{_bindir}/WidgetsCxxTests
%{_bindir}/finance

%files -n tcl-%{name}
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/vtk
%attr(0755,root,root) %{_libdir}/libvtk*TCL*.so.* 
%{_libdir}/vtk-*/tcl
%{_libdir}/vtk-*/*.tcl
%dir %{_libdir}/vtk-*/testing
%{_libdir}/vtk-*/testing/*.tcl
%doc README.html 
%doc vtkLogo.jpg

%files -n tcl-%{name}-devel
%defattr(0755,root,root,0755)
%{_bindir}/vtkWrapTcl
%{_bindir}/vtkWrapTclInit
%{_libdir}/libvtk*TCL*.so

%files -n python-%{name}
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/vtkpython
%attr(0755,root,root) %{_libdir}/libvtk*Python*.so.*
%dir %{_libdir}/vtk-*/testing
%{_libdir}/vtk-*/testing/*.py
%{python_sitelib}/vtk
%{python_sitelib}/VTK-*.egg-info

%files -n python-%{name}-devel
%defattr(0755,root,root,0755)
%{_bindir}/vtkWrapPython
%{_bindir}/vtkWrapPythonInit
%{_libdir}/libvtk*Python*.so

%files -n %{libname}-qt
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/qtevents
%attr(0755,root,root) %{_bindir}/qtimageviewer
%attr(0755,root,root) %{_bindir}/qtsimpleview
%attr(0755,root,root) %{_libdir}/libQVTK.so.*
%attr(0755,root,root) %{qt_designer_plugins_dir}/libQVTKWidgetPlugin.so

%if %build_java
%files -n java-%{name}
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/vtkParseJava
%attr(0755,root,root) %{_bindir}/vtkWrapJava
%{_bindir}/VTKJavaExecutable
%attr(0755,root,root) %{_libdir}/libvtk*Java.so*
%{_libdir}/vtk/java
%endif

%files examples
%defattr(0644,root,root,0755)
%dir %{_datadir}/vtk-examples
%{_datadir}/vtk-examples/Examples
%{_datadir}/vtk-examples/Testing

%files doc
%defattr(0644,root,root,0755)
%{_datadir}/vtk-docs/api

%clean 
rm -rf %{buildroot}
