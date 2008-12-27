# TODO: - test the java build
#define _disable_ld_no_undefined	1
#define _disable_ld_as_needed		1

%define build_java	0
%{?_with_java: %{expand: %%global build_java 1}}

%define short_version	%(echo %{version} | cut -d. -f1,2)

%define libname		%mklibname %{name}
%define libname_devel	%mklibname %{name} -d

%define qt_designer_plugins_dir	%{qt4plugins}/designer

Summary:	Toolkit for 3D computer graphics, image processing, and visualization
Name:		vtk
Version:	5.2.0
Release:	%{mkrel 2}
License:	BSD
Group:		Graphics
URL:		http://public.kitware.com/VTK/
Source0:	http://www.vtk.org/files/release/%{short_version}/vtk-%{version}.tar.gz
# fix qt method calls in python
Patch0:		vtk-python-qt.patch
Patch1:		vtk-vtkLoadPythonTkWidgets.patch
# tcl/tk 8.6 headers
Source10:	vtk-5.2.0-tk86headers.tar.lzma
Patch2:		vtk-tcl8.5.patch
# fixes for gcc 4.3
Patch3:		vtk-gcc4.3.patch
# install libs to libdir not /usr/lib/vtk; install cmake crap to
# libdir/vtk . libs in /usr/lib/vtk don't work as ld can't find them.
# install TCL stuff to tcl_sitearch. FIXME: hardcodes tcl version
# - AdamW 2008/10
Patch4:		vtk-5.2.0-install_locations.patch
Patch5:		vtk-fix-underlink.patch
# work with tcl 8.6 (this is a hack, not a proper fix, issue has been
# reported upstream: http://www.vtk.org/Bug/view.php?id=7822) - AdamW
# 2008/10
Patch6:		vtk-5.2.0-tcl8.6.patch
# Fix pkgIndex.tcl so TCL stuff can be in a different place from
# the libs, and also to load the versioned (.so.version) lib files
# rather than plain .so. FIXME: hardcodes /usr . should be as easy
# as using @VTK_INSTALL_ROOT@, but it isn't. - AdamW 2008/10
Patch7:		vtk-5.2.0-tcl_relocate.patch
# BioImageXD contains classes to read lsm files (from zeiss)
Source1:	BioImageXD.tar.bz2
# do not install widgets
Patch8:		vtk-bioimagexd-widgets.patch
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
BuildRequires:	tcl
BuildRequires:	tk
BuildRequires:	qt4-devel
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

NOTE: The java wrapper is not included by default.  You may rebuild the srpm
      using "--with java" with JDK installed.


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

%if %build_java
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
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0
%patch6 -p1
%patch7 -p1

# for tcl/tk 8.6
pushd Utilities/TclTk
tar xf %{SOURCE10}
popd

# fix data path
find -type f | xargs sed -i -e 's#../../../../VTKData#%{_datadir}/vtk-data#g'

# install extra classes from BioImageXD
tar xf %{SOURCE1}
pushd BioImageXD
rm -rf `find -type d -name .svn`
%patch8
sh bin/install_classes.sh . ..
popd

%build
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
	-DVTK_BUILD_PREFIX=%{_prefix}

%if %build_java
cmake	-DJAVA_INCLUDE_PATH:PATH=$JAVA_HOME/include \
	-DJAVA_INCLUDE_PATH2:PATH=$JAVA_HOME/include/linux \
	-DJAVA_AWT_INCLUDE_PATH:PATH=$JAVA_HOME/include \
	-DJAVA_AWT_LIBRARY:PATH=$JAVA_HOME/jre/lib/i386/libawt.so \
	-DVTK_WRAP_JAVA:BOOL=ON \
.
%endif

%make
# build docs
(
cd Utilities/Doxygen
make DoxygenDoc
)

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} -C build

%if %build_java
#install java
install -d -m 755 %{buildroot}%{_libdir}/vtk/java
install -m 644 lib/vtk.jar     %{buildroot}%{_libdir}/vtk/java
install -m 644 java/vtk/*.java %{buildroot}%{_libdir}/vtk/java
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
rm -f test-suite-files
(
cd build/bin
for f in `find -type f | grep -v '.so$' | grep -v vtk`; do
   install -m0755 $f %{buildroot}%{_bindir}
done
)
rm -f %{buildroot}%{_bindir}/*.so.*
%multiarch_includes  %{buildroot}%{_includedir}/vtk-%{short_version}/vtkConfigure.h
%multiarch_includes  %{buildroot}%{_includedir}/vtk-%{short_version}/vtknetcdf/ncconfig.h

# drop files which which shouldn't be there
rm -rf %{buildroot}/TclTk
rm -rf %{buildroot}%{_libdir}/vtk-%{short_version}/doc

# move test tcl files to the tcl location
mkdir -p %{buildroot}%{tcl_sitearch}/vtk-%{short_version}/testing
mv %{buildroot}%{_libdir}/vtk-%{short_version}/testing/*.tcl %{buildroot}%{tcl_sitearch}/vtk-%{short_version}/testing

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
%{_libdir}/lib*.so.*
%exclude %{_libdir}/libvtk*TCL*.so.*
%exclude %{_libdir}/libvtk*Python*.so.*
%exclude %{_libdir}/libQVTK.so.*
%exclude %{_libdir}/libvtk*Java.so.*

%files -n %{libname_devel}
%defattr(0644,root,root,0755)
%{_includedir}/*
%dir %{_libdir}/vtk-%{short_version}
%{_libdir}/vtk-%{short_version}/*.cmake
%{_libdir}/vtk-%{short_version}/CMake
%{_libdir}/vtk-%{short_version}/doxygen
%{_libdir}/vtk-%{short_version}/hints
%{_libdir}/lib*.so
%exclude %{_libdir}/libvtk*TCL*.so
%exclude %{_libdir}/libvtk*Python*.so
%exclude %{_libdir}/libvtk*Java.so
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
%{_bindir}/CreateTree
%{_bindir}/Example1
%{_bindir}/Example2
%{_bindir}/HelloWorld
%{_bindir}/HybridCxxTests
%{_bindir}/ImageSlicing
%{_bindir}/InfovisCxxTests
%{_bindir}/MaterialObjects
%{_bindir}/MultiView
%{_bindir}/ParallelCxxTests
%{_bindir}/ProcessShader
%{_bindir}/ProcessShader-real
%{_bindir}/QVTKCxxTests
%{_bindir}/TestFBOImplementation
%{_bindir}/Theme
%{_bindir}/TimeRenderer
%{_bindir}/TimeRenderer2
%{_bindir}/TreeLayout
%{_bindir}/ViewsCxxTests

%files -n tcl-%{name}
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/vtk
%attr(0755,root,root) %{_libdir}/libvtk*TCL*.so.* 
%{tcl_sitearch}/vtk-%{short_version}
%doc README.html vtkLogo.jpg

%files -n tcl-%{name}-devel
%defattr(0755,root,root,0755)
%{_bindir}/vtkWrapTcl
%{_bindir}/vtkWrapTclInit
%attr(0755,root,root) %{_libdir}/libvtk*TCL*.so 

%files -n python-%{name}
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/vtkpython
%attr(0755,root,root) %{_libdir}/libvtk*Python*.so.*
%dir %{_libdir}/vtk-%{short_version}/testing
%{_libdir}/vtk-%{short_version}/testing/*.py
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
%attr(0755,root,root) %{_bindir}/VTKJavaExecutable
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
