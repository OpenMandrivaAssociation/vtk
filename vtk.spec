#define _unpackaged_files_terminate_build 0

#define _disable_ld_no_undefined 1
#define _disable_lto 1

%bcond_with OSMesa
# Documentation are download and built by vtk-doc separated package
%bcond_without java

%define libname %mklibname %{name}
%define libname_devel %mklibname %{name} -d

%define short_version %(echo %{version} | cut -d. -f1,2)

%define vtkincdir %{_includedir}/vtk
%define vtkdocdir %{_docdir}/vtk
%define vtktcldir %{tcl_sitearch}/%{name}-%{short_version}

%define qt_designer_plugins_dir %{_libdir}/qt5/plugins/designer

Name:		vtk
Version:	8.2.0
Release:	3
Summary:	Toolkit for 3D computer graphics, image processing, and visualization
License:	BSD
Group:		Graphics
URL:		http://www.vtk.org/
Source0:	http://www.vtk.org/files/release/%{short_version}/VTK-%{version}.tar.gz
Source1:	http://www.vtk.org/files/release/%{short_version}/VTKData-%{version}.tar.gz
# dont build/install wrapper tools for wrappers which are not
# built
#Patch1:	vtk-8.1.2-wrap.patch
#https://gitlab.kitware.com/vtk/vtk/merge_requests/5883.patch
Patch0:		5883.patch
Patch1:		vtk-8.2.0-compile.patch

BuildRequires:	cmake >= 1.8 
BuildRequires:	double-conversion-devel
BuildRequires:	expat-devel >= 2.0.1
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	tiff-devel
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5X11Extras)
BuildRequires:	pkgconfig(Qt5OpenGL)
BuildRequires:	pkgconfig(Qt5Sql)
BuildRequires:	pkgconfig(Qt5WebKitWidgets)
BuildRequires:	pkgconfig(Qt5UiTools)
BuildRequires:	cmake(ECM)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(eigen3)
BuildRequires:	chrpath
BuildRequires:	pkgconfig(liblz4)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(netcdf)
BuildRequires:	pkgconfig(jsoncpp)
BuildRequires:	pkgconfig(sqlite3)
#BuildRequires:  pkgconfig(proj)
BuildRequires:	perl
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	tk-devel >= 8.5
BuildRequires:	tcl-devel >= 8.5
BuildRequires:	libxml2-devel
BuildRequires:	boost-devel
BuildRequires:	python3-devel
BuildRequires:	python-sip
BuildRequires:	hdf5-devel
BuildRequires:	pugixml-devel
%if %{with java}
BuildRequires:	jdk-current
BuildRequires:	java-gui-current
%endif
BuildRequires:	blas-devel
BuildRequires:	lapack-devel

Obsoletes:	vtk-data < 8.2.0
Obsoletes:	vtk-examples < 8.2.0
Obsoletes:	%{name}-tcl < 8.2.0

# Do not check .so files in the python_sitearch directory
%global __provides_exclude_from ^%{python_sitearch}/.*\\.so$

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

%if ! %{with java}
NOTE: The java wrapper is not included by default.  You may rebuild the srpm
      using "--with java" with JDK installed.
%endif

#------------------------------------------------------------------------------

%package -n %{libname}
Summary:	Toolkit for 3D computer graphics, image processing, and visualization
Group:		System/Libraries
Provides:	%{name} = %{EVRD}
Obsoletes:	%{name} < %{EVRD}

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

%if ! %{with java}
NOTE: The java wrapper is not included by default.  You may rebuild the srpm
      using "--with java" with JDK installed.
%endif

%files -n %{libname}
%doc Copyright.txt vtkBanner.gif
%dir %{_libdir}/vtk
%{_libdir}/vtk/libvtk*

#------------------------------------------------------------------------------

%package -n %{libname_devel}
Summary:	VTK header files for building C++ code
Requires:	%{libname} = %{EVRD}
Group:		Development/C++
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{name}-devel < %{EVRD}
Conflicts:	%{libname}-qt < 5.0.3-4
Conflicts:	%{libname} < 5.6.1-2
Requires:	%{libname}-qt = %{version}-%{release}
Requires:	python-%{name} >= %{EVRD}
%if %{with java}
Requires:	java-%{name} >= %{EVRD}
%endif

%description -n %{libname_devel}
This provides the VTK header files required to compile C++
programs that use VTK to do 3D visualisation.

%files -n %{libname_devel}
%doc Utilities/Upgrading
%{_bindir}/vtkWrapHierarchy*
%{_includedir}/*
%{_libdir}/vtk/*.so
%{_libdir}/vtk/libvtkWrappingTools.a
%{_libdir}/cmake/vtk/
%{_docdir}/vtk-8.2/

#------------------------------------------------------------------------------

%package -n python-%{name}
Summary:	Python bindings for VTK
Requires:	%{libname} = %{version}
Group:		Development/Python
Obsoletes:	%{name}-python < %{version}
Obsoletes:	python-%{name}-devel < %{version}
Provides:	%{name}-python = %{version}

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
%{_libdir}/vtk/*Python38D.so.*
%exclude %{_libdir}/vtk/*QtPython38D.so.*
%{_bindir}/vtkpython
%{_bindir}/vtkWrapPython
%{_bindir}/vtkWrapPythonInit
%optional %{python_sitearch}/__pycache__/*
%{python_sitearch}/vtkmodules
%{python_sitearch}/vtk.py

#------------------------------------------------------------------------------

%package -n %{libname}-qt
Summary:	QT VTK widget
Requires:	vtk
Group:		System/Libraries

%description -n %{libname}-qt
The vtkQt classes combine VTK and Qt(TM) for X11.

%files -n %{libname}-qt
%{_libdir}/vtk/lib*Qt*.so.*
%exclude %{_libdir}/vtk/*Python38D.so.*
%{_libdir}/qt5/plugins/designer/libQVTKWidgetPlugin.so

%package -n python-vtk-qt
Summary:	Qt Python bindings for VTK
Requires:	vtk = %{EVRD}
Group:		System/Libraries

%description -n python-vtk-qt
Qt Python bindings for VTK.

%files -n python-vtk-qt
%{_libdir}/vtk/*QtPython38D.so.*

#------------------------------------------------------------------------------

%if %{with java}
%package -n java-%{name}
Summary:	Java bindings for VTK
Group:		Development/Java
Requires:	%{libname} = %{version}
Obsoletes:	%{name}-java < %{version}
Provides:	%{name}-java = %{version}

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
%_bindir/vtkParseJava
%_bindir/vtkWrapJava
%_libdir/vtk/vtk.jar
%endif
#------------------------------------------------------------------------------

%package test-suite
Summary:	Tests programs for VTK
Requires:	%{libname} = %{version}
Group:		Development/Other

%description test-suite
This package contains all testing programs from the VTK
source. The source code of these programs can be found in the
vtk-examples package.

%files test-suite
%_bindir/*
%exclude %{_bindir}/vtkpython
%exclude %{_bindir}/vtkWrapPython
%exclude %{_bindir}/vtkWrapPythonInit
%exclude %{_bindir}/vtkWrapHierarchy

#------------------------------------------------------------------------------

%prep
%autosetup -p1 -n VTK-%{version}

# Replace relative path ../../../VTKData with %{_datadir}/vtkdata-%{version}
# otherwise it will break on symlinks.
grep -rl '\.\./\.\./\.\./\.\./VTKData' . | xargs \
  perl -pi -e's,\.\./\.\./\.\./\.\./VTKData,%{_datadir}/vtkdata-%{version},g'

%build
export CFLAGS="%{optflags} -D_UNICODE"
export CXXFLAGS="%{optflags} -D_UNICODE"
%if %{with java}
. %{_sysconfdir}/profile.d/90java.sh
%endif

# Remove old cmake files
rm -f CMake/FindBoost*

# Due to cmake prefix point already for _prefix, we need
# push only the necessary extra paths

%cmake \
	-DVTK_INSTALL_LIBRARY_DIR=%{_lib}/vtk \
	-DVTK_INSTALL_ARCHIVE_DIR=%{_lib}/vtk \
	-DVTK_INSTALL_BIN_DIR=/bin \
	-DVTK_INSTALL_PACKAGE_DIR=%{_lib}/vtk \
	-DVTK_PYTHON_VERSION=3 \
	-DVTK_INSTALL_PYTHON_MODULES_DIR:PATH=%{python_sitearch} \
	-DVTK_INSTALL_INCLUDE_DIR=include/vtk \
	-DVTK_QT_VERSION=5 \
	-DVTK_CUSTOM_LIBRARY_SUFFIX="" \
	-DVTK_INSTALL_PACKAGE_DIR:PATH=%{_lib}/cmake/vtk \
	-DVTK_INSTALL_QT_DIR:PATH=%{_lib}/qt5/plugins/designer \
	-DVTK_INSTALL_TCL_DIR:PATH=share/tcl%{tcl_version}/vtk \
	-DTK_INTERNAL_PATH:PATH=/usr/include/tk-private/generic \
%if %{with OSMesa}
	-DVTK_OPENGL_HAS_OSMESA:BOOL=ON \
%endif
	-DVTK_DATA_ROOT=/share/vtk \
	-DVTK_USE_SYSTEM_LIBPROJ4:BOOL=OFF \
	-DVTK_USE_SYSTEM_LIBPROJ:BOOL=OFF \
	-DVTK_WRAP_PYTHON:BOOL=ON \
%if %{with java}
	-DJAVA_INCLUDE_PATH:PATH=$JAVA_HOME/include \
	-DJAVA_INCLUDE_PATH2:PATH=$JAVA_HOME/include/linux \
	-DJAVA_AWT_INCLUDE_PATH:PATH=$JAVA_HOME/include \
	-DVTK_WRAP_JAVA:BOOL=ON \
%else
	-DVTK_WRAP_JAVA:BOOL=OFF \
%endif
	-DVTK_WRAP_TCL:BOOL=ON \
	-DVTK_Group_Imaging:BOOL=ON \
	-DVTK_Group_Qt:BOOL=ON \
	-DVTK_Group_Rendering:BOOL=ON \
	-DVTK_Group_StandAlone:BOOL=ON \
	-DVTK_Group_Tk:BOOL=ON \
	-DVTK_Group_Views:BOOL=ON \
	-DModule_vtkFiltersStatisticsGnuR:BOOL=ON \
	-DModule_vtkTestingCore:BOOL=ON \
	-DModule_vtkTestingRendering:BOOL=ON \
	-DVTK_USE_RENDERING:BOOL=ON \
	-DVTK_USE_QT:BOOL=ON \
	-DBUILD_DOCUMENTATION:BOOL=OFF \
	-DBUILD_EXAMPLES:BOOL=ON \
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DBUILD_TESTING:BOOL=OFF \
	-DVTK_USE_SYSTEM_EXPAT:BOOL=ON \
	-DVTK_USE_SYSTEM_JPEG:BOOL=ON \
	-DVTK_USE_SYSTEM_PNG:BOOL=ON \
	-DVTK_USE_SYSTEM_TIFF:BOOL=ON \
	-DVTK_USE_SYSTEM_ZLIB:BOOL=ON \
	-DVTK_USE_SYSTEM_FREETYPE:BOOL=ON \
	-DVTK_USE_SYSTEM_LIBHARU=OFF \
	-DVTK_USE_ANSI_STDLIB:BOOL=ON \
	-DVTK_USE_PARALLEL:BOOL=ON \
	-DVTK_USE_GUISUPPORT:BOOL=ON \
	-DVTK_USE_QVTK:BOOL=ON \
	-DVTK_PYTHON_SETUP_ARGS:STRING="--prefix=%{_prefix} --root=%{buildroot}" \
	-DVTK_INSTALL_QT_PLUGIN_DIR:STRING=%{qt_designer_plugins_dir} \
	-DVTK_USE_GL2PS:BOOL=ON \
	-DVTK_HAVE_GETSOCKNAME_WITH_SOCKLEN_T:INTERNAL=1 \
	-DVTK_USE_SYSTEM_LIBXML2:BOOL=ON \
	-DVTK_USE_QVTK_QTOPENGL:BOOL=ON \
	-DVTK_USE_OGGTHEORA_ENCODER=ON \
	-DVTK_USE_SYSTEM_LIBRARIES=ON \
	-DVTK_USE_SYSTEM_NETCDFCPP=OFF \
	-DVTK_USE_SYSTEM_GL2PS=OFF \
	-DVTK_USE_BOOST:BOOL=ON \
	-G Ninja
%ninja_build


%install
%ninja_install -C build

#remove la files
find %{buildroot}%{_libdir} -name *.la -delete
