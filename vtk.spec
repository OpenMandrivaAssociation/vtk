#define _unpackaged_files_terminate_build 0

# /CMakeFiles/exodusII.dir/src/ex_update.c.o ThirdParty/exodusII/vtkexodusII/CMakeFiles/exodusII.dir/src/ex_utils.c.o  -lpthread  /usr/lib64/libnetcdf.so && :
# ld: error: undefined symbol: H5get_libversion
%define _disable_ld_no_undefined 1

# (tpg) get rid of weird cmake provides, also doubled with system wide ones
%global __provides_exclude ^cmake\\(.*)$

# (tpg) either you have X11 or OSMesa, you can not have both
%bcond_with OSMesa
# Documentation are download and built by vtk-doc separated package
%bcond_without java

%ifarch %aarch64
%bcond_without gles
%else
%bcond_with    gles
%endif

%define libname %mklibname %{name}
%define libname_devel %mklibname %{name} -d

%define short_version %(echo %{version} | cut -d. -f1,2)

%define vtkincdir %{_includedir}/vtk
%define vtkdocdir %{_docdir}/vtk
%define vtktcldir %{tcl_sitearch}/%{name}-%{short_version}

%define qt_designer_plugins_dir %{_libdir}/qt5/plugins/designer

# Workaround for the dependency generator not being able to
# expand all cmake variables
# Avoids dependency on
# (cmake("python${vtk_python_version}") or cmake("Python${VTK_PYTHON_VERSION}"))
%global __requires_exclude  ^(.*)cmake(.*)Python(.*)$

Name:		vtk
Version:	9.1.0
Release:	3
Summary:	Toolkit for 3D computer graphics, image processing, and visualization
License:	BSD
Group:		Graphics
URL:		http://www.vtk.org/
Source0:	http://www.vtk.org/files/release/%{short_version}/VTK-%{version}.tar.gz
Source1:	http://www.vtk.org/files/release/%{short_version}/VTKData-%{version}.tar.gz
# Header-only library, not presently used by anything else...
Source2:	https://raw.githubusercontent.com/ArashPartow/exprtk/master/exprtk.hpp
# (tpg) our libharu is good
Patch2:		VTK-9.0.0-fix-libharu-version.patch
Patch3:		vtk-9.1.0-workaround-libstdc++-clang-incompatibility.patch
Patch4:		VTK-9.1.0-glx-linkage.patch

%if %{with gles}
# Patches for gles/aarch64 imported from ŁopenSUSE
Patch7:         0001-Add-missing-guard-required-for-GLES-to-disable-stere.patch
# PATCH-FIX-UPSTREAM -- Fix building with Qt GLES builds
Patch8:         0001-Correct-GL_BACK-GL_BACK_LEFT-mapping-on-GLES.patch
# PATCH-FIX-UPSTREAM -- Fix building with Qt GLES builds
Patch9:         0002-Use-GL_DRAW_BUFFER0-instead-of-GL_DRAW_BUFFER-for-GL.patch
# PATCH-FIX-UPSTREAM
Patch10:        0001-GL_POINT_SPRITE-is-only-available-for-Compatibility-.patch
%endif

BuildRequires:	double-conversion-devel >= 3.1.5
BuildRequires:	pkgconfig(expat) >= 2.0.1
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(zlib)
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
BuildRequires:  pkgconfig(proj)
BuildRequires:	pkgconfig(fmt)
BuildRequires:	utf8cpp-devel >= 3.1.1
BuildRequires:	pegtl-devel
BuildRequires:	gl2ps-devel
BuildRequires:	pkgconfig(proj)
BuildRequires:	perl
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	pkgconfig(tk) >= 8.5
BuildRequires:	pkgconfig(tcl) >= 8.5
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(python)
BuildRequires:	python-sip
BuildRequires:	hdf5-devel
BuildRequires:	pugixml-devel
BuildRequires:	libharu-devel
%if %{with java}
BuildRequires:	jdk-current
BuildRequires:	java-gui-current
%endif
BuildRequires:	pkgconfig(blas)
BuildRequires:	pkgconfig(lapack)

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
%{_libdir}/libvtk*.so.*
# Qt is a separate package
%exclude %{_libdir}/libvtkGUISupportQt.so.*
%exclude %{_libdir}/libvtkGUISupportQtSQL.so.*
%exclude %{_libdir}/libvtkRenderingQt.so.*
%exclude %{_libdir}/libvtkViewsQt.so.*
# Python is a separate package
%exclude %{_libdir}/libvtkCommonPython.so.*
%exclude %{_libdir}/libvtkFiltersPython.so.*
%exclude %{_libdir}/libvtkPythonContext2D.so.*
%exclude %{_libdir}/libvtkPythonInterpreter.so.*
%{_libdir}/vtk

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
Requires:	%{name}-test-suite >= %{EVRD}
%if %{with java}
Requires:	java-%{name} >= %{EVRD}
%endif

Requires:	double-conversion-devel >= 3.1.5
Requires:	pkgconfig(expat) >= 2.0.1
Requires:	pkgconfig(libjpeg)
Requires:	pkgconfig(libpng)
Requires:	pkgconfig(libtiff-4)
Requires:	pkgconfig(zlib)
Requires:	pkgconfig(Qt5Core)
Requires:	pkgconfig(Qt5Gui)
Requires:	pkgconfig(Qt5Widgets)
Requires:	pkgconfig(Qt5X11Extras)
Requires:	pkgconfig(Qt5OpenGL)
Requires:	pkgconfig(Qt5Sql)
Requires:	pkgconfig(Qt5WebKitWidgets)
Requires:	pkgconfig(Qt5UiTools)
Requires:	cmake(ECM)
Requires:	pkgconfig(freetype2)
Requires:	pkgconfig(egl)
Requires:	pkgconfig(gl)
Requires:	pkgconfig(glew)
Requires:	pkgconfig(eigen3)
Requires:	pkgconfig(liblz4)
Requires:	pkgconfig(x11)
Requires:	pkgconfig(xt)
Requires:	pkgconfig(theora)
Requires:	pkgconfig(netcdf)
Requires:	pkgconfig(jsoncpp)
Requires:	pkgconfig(sqlite3)
Requires:	utf8cpp-devel >= 3.1.1
Requires:	pegtl-devel
Requires:	gl2ps-devel
Requires:	pkgconfig(proj)
Requires:	graphviz
Requires:	pkgconfig(tk) >= 8.5
Requires:	pkgconfig(tcl) >= 8.5
Requires:	pkgconfig(libxml-2.0)
Requires:	boost-devel
Requires:	pkgconfig(python)
Requires:	python-sip
Requires:	hdf5-devel
Requires:	pugixml-devel
Requires:	libharu-devel
Requires:	pkgconfig(blas)
Requires:	pkgconfig(lapack)

%description -n %{libname_devel}
This provides the VTK header files required to compile C++
programs that use VTK to do 3D visualisation.

%files -n %{libname_devel}
%doc Utilities/Upgrading
%doc %{_datadir}/licenses/VTK
%{_bindir}/vtkWrapHierarchy*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/%{name}

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
%{_bindir}/vtkpython
%{_bindir}/vtkWrapPython
%{_bindir}/vtkWrapPythonInit
%{_libdir}/libvtkCommonPython.so.*
%{_libdir}/libvtkFiltersPython.so.*
%{_libdir}/libvtkPythonContext2D.so.*
%{_libdir}/libvtkPythonInterpreter.so.*
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
%{_libdir}/libvtkGUISupportQt.so.*
%{_libdir}/libvtkGUISupportQtSQL.so.*
%{_libdir}/libvtkRenderingQt.so.*
%{_libdir}/libvtkViewsQt.so.*
%{_libdir}/qml/VTK.*

%package -n python-vtk-qt
Summary:	Qt Python bindings for VTK
Requires:	vtk = %{EVRD}
Group:		System/Libraries

%description -n python-vtk-qt
Qt Python bindings for VTK.

%files -n python-vtk-qt

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
%_libdir/java/vtk.jar
%{_libdir}/java/vtk-*
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

# (tpg) remove 3rd party software
for x in vtk{doubleconversion,eigen,expat,freetype,gl2ps,glew,hdf5,jpeg,jsoncpp,libharu,libproj,libxml2,lz4,lzma,mpi4py,netcdf,ogg,pegtl,png,pugixml,sqlite,theora,tiff,utf8,zfp,zlib}
do
  rm -r ThirdParty/*/${x}
done

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
	-DVTK_VERSIONED_INSTALL:BOOL=OFF \
	-DVTK_GROUP_ENABLE_Qt=YES \
	-DVTK_GROUP_ENABLE_Web=YES \
	-DVTK_GROUP_ENABLE_Views=YES \
	-DVTK_GROUP_ENABLE_Imaging=YES \
	-DVTK_QT_VERSION=5 \
	-DVTK_CUSTOM_LIBRARY_SUFFIX="" \
	-DVTK_INSTALL_PACKAGE_DIR:PATH=%{_lib}/cmake/vtk \
	-DVTK_INSTALL_QT_DIR:PATH=%{_lib}/qt5/plugins/designer \
	-DVTK_INSTALL_TCL_DIR:PATH=share/tcl%{tcl_version}/vtk \
	-DTK_INTERNAL_PATH:PATH=/usr/include/tk-private/generic \
	-DExprTk_INCLUDE_DIR=${RPM_SOURCE_DIR} \
	-DQMLPLUGINDUMP_EXECUTABLE=%{_libdir}/qt5/bin/qmlplugindump \
%if %{with OSMesa}
	-DVTK_OPENGL_HAS_OSMESA:BOOL=ON \
%endif
	-DVTK_OPENGL_USE_GLES:BOOL=%{?with_gles:ON}%{!?with_gles:OFF} \
	-DVTK_DATA_ROOT=/share/vtk \
	-DVTK_USE_SYSTEM_LIBPROJ4:BOOL=ON \
	-DVTK_USE_SYSTEM_LIBPROJ:BOOL=ON \
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
	-DVTK_USE_EXTERNAL=ON \
	-DVTK_USE_SYSTEM_LIBRARIES=ON \
	-DVTK_MODULE_USE_EXTERNAL_VTK_cgns=OFF \
	-DVTK_MODULE_USE_EXTERNAL_VTK_ioss=OFF \
	-DVTK_USE_SYSTEM_NETCDFCPP=OFF \
	-DVTK_USE_SYSTEM_GL2PS=ON \
	-DVTK_USE_BOOST:BOOL=ON \
	-DINSTALL_PKG_CONFIG_MODULE:BOOL=ON \
	-DVTK_JAVA_SOURCE_VERSION=17 \
	-DVTK_JAVA_TARGET_VERSION=17 \
	-DVTK_FORBID_DOWNLOADS=ON \
	-G Ninja
export LD_LIBRARY_PATH="$(pwd)/%{_lib}"
export QT_QPA_PLATFORM=offscreen
%ninja_build


%install
%ninja_install -C build

#remove la files
find %{buildroot}%{_libdir} -name *.la -delete

