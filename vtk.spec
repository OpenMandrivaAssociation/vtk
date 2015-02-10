# Documentation are download and built by vtk-doc separated package
%bcond_with java

%define libname		%mklibname %{name}
%define libname_devel	%mklibname %{name} -d

%define bioxd_version	0.20111111
%define short_version	%(echo %{version} | cut -d. -f1,2)

%define vtkincdir	%{_includedir}/vtk
%define vtkdocdir	%{_docdir}/vtk
%define vtktcldir	%{tcl_sitearch}/%{name}-%{short_version}

%define qt_designer_plugins_dir	%{qt4plugins}/designer

Name:		vtk
Version:	5.10.1
Release:	9
Summary:	Toolkit for 3D computer graphics, image processing, and visualization
License:	BSD
Group:		Graphics
URL:		http://www.vtk.org/
Source0:	http://www.vtk.org/files/release/%{short_version}/vtk-%{version}.tar.gz
Source1:	http://www.vtk.org/files/release/%{short_version}/vtkdata-%{version}.tar.gz

# BioImageXD contains classes to read lsm files (from zeiss)
#URL:		http://www.bioimagexd.net
# svn co https://bioimagexd.svn.sourceforge.net/svnroot/bioimagexd/bioimagexd/trunk BioImageXD
# cd BioImageXD
# rm -fr `find . -type d -name .svn`
# rm -f bin/ffmpeg.exe bin/ffmpeg.osx bin/*.bat bin/*.dll bin/*.manifest bin/*.iss
# cd ..
# tar jcvf BioImageXD-0.`date +%\Y%\m%\d`.tar.bz2 BioImageXD
Source2:	BioImageXD-%{bioxd_version}.tar.bz2
Source100:	vtk.rpmlintrc

# fix qt method calls in python
Patch0:		vtk-5.8.0-python-qt.patch
Patch1:		vtk-5.8.0-vtkLoadPythonTkWidgets.patch
Patch2:		vtk-5.8.0-tcl8.6.patch
Patch3:		vtk-5.10.1-fix-underlink.patch
Patch4:		vtk-5.10.1-soversion.patch

Patch5:		vtk-BioImageXD-0.20111111-widgets.patch
Patch6:		vtk-5.8.0-BioImageXD-visibility.patch
Patch7:		vtk-5.10.1-share-dir.patch

BuildRequires:	cmake >= 1.8
BuildRequires:	expat-devel >= 2.0.1
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	tiff-devel
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xt)
BuildRequires:	perl
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	cvs
BuildRequires:	gnuplot
BuildRequires:	qt4-devel
BuildRequires:	tk-devel >= 8.6
BuildRequires:	tcl-devel >= 8.6
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	boost-devel
BuildRequires:	python-devel
%if %with java
BuildRequires:	java-rpmbuild
BuildRequires:	java-devel > 1.5
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
%{_libdir}/lib*.so.*
%exclude %{_libdir}/libvtk*TCL*.so.*
%exclude %{_libdir}/libvtk*Python*.so.*
%exclude %{_libdir}/libQVTK.so.*
%if %with java
%exclude %{_libdir}/libvtk*Java.so.*
%endif

#------------------------------------------------------------------------------

%package -n %{libname_devel}
Summary:	VTK header files for building C++ code
Requires:	%{libname} = %{version}
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel < %{version}-%{release}
Conflicts:	%{libname}-qt < 5.0.3-4
Conflicts:	%{libname} < 5.6.1-2
Requires:	%{libname}-qt = %{version}-%{release}

%description -n %{libname_devel}
This provides the VTK header files required to compile C++
programs that use VTK to do 3D visualisation.

%files -n %{libname_devel}
%defattr(0644,root,root,0755)
%{_includedir}/*
%dir %{_libdir}/vtk/
# FIXME install these as is due to how it resolves some cmake macros based on
# location of these files
%{_libdir}/*.cmake
%{_libdir}/vtk/*
%{_libdir}/lib*.so
%exclude %{_libdir}/libvtk*TCL*.so
%exclude %{_libdir}/vtk/testing/*.tcl
%exclude %{_libdir}/libvtk*Python*.so
%exclude %{_libdir}/vtk/testing/*.py
%if %with java
%exclude %{_libdir}/libvtk*Java.so
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
%attr(0755,root,root) %{_bindir}/%{name}
%attr(0755,root,root) %{_libdir}/libvtk*TCL*.so.* 
%{_libdir}/vtk/testing/*.tcl
%{_libdir}/tcl
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
%{_bindir}/vtkWrapTcl
%{_bindir}/vtkWrapTclInit
%{_libdir}/*.tcl
%attr(0755,root,root) %{_libdir}/libvtk*TCL*.so 

#------------------------------------------------------------------------------

%package -n python-%{name}
Summary:	Python bindings for VTK
Requires:	%{libname} = %{version}
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
%defattr(0755,root,root,0755)
%{_bindir}/vtkpython
%{_libdir}/libvtk*Python*.so.*
%{_libdir}/vtk/testing/*.py
%defattr(0644,root,root,0755)
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
%{_bindir}/vtkWrapPython
%{_bindir}/vtkWrapPythonInit
%{_libdir}/libvtk*Python*.so

#------------------------------------------------------------------------------

%package -n %{libname}-qt
Summary:	QT VTK widget
Requires:	vtk
Group:		System/Libraries

%description -n %{libname}-qt
The vtkQt classes combine VTK and Qt(TM) for X11.

%files -n %{libname}-qt
%defattr(0644,root,root,0755)
%{_bindir}/qtevents
%{_bindir}/qtimageviewer
%attr(0755,root,root) %{_libdir}/libQVTK.so.*
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
%{_bindir}/vtkParseJava
%{_bindir}/vtkWrapJava
%{_bindir}/VTKJavaExecutable
%{_libdir}/libvtk*Java.so*
%{_libdir}/java

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
%{_datadir}/vtk

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
%{_bindir}/*
%exclude %{_bindir}/%{name}
%exclude %{_bindir}/vtkWrapTcl
%exclude %{_bindir}/vtkWrapTclInit
%exclude %{_bindir}/vtkpython
%exclude %{_bindir}/vtkWrapPython
%exclude %{_bindir}/vtkWrapPythonInit
%exclude %{_bindir}/qtevents
%exclude %{_bindir}/qtimageviewer

#------------------------------------------------------------------------------

%prep
%setup -q -n VTK%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch7 -p1

# fix data path
find . -type f | xargs sed -i -e 's|../../../../VTKData|%{_datadir}/vtk|g'

# install extra classes from BioImageXD
tar xf %{SOURCE2}
pushd BioImageXD
%patch5 -p0
sh bin/install_classes.sh . ..
popd

%patch6 -p1

for f in  {vtkImageAutoThresholdColocalization,vtkIntensityTransferFunction}.{cxx,h}; do
    mv -f BioImageXD/vtkBXD/Processing/$f Filtering
    ln -sf Filtering/$f BioImageXD/vtkBXD/Processing
done
mv -f BioImageXD/vtkBXD/Processing/vtkBXDProcessingWin32Header.h Filtering
ln -sf Filtering/vtkBXDProcessingWin32Header.h BioImageXD/vtkBXD/Processing
sed -e 's|cmakedefine|define|' BioImageXD/vtkBXD/VTKBXDConfigure.h.in > Filtering/VTKBXDConfigure.h

for f in  {vtkImageLabelAverage,vtkImageSolitaryFilter,vtkImageSimpleMIP,vtkImageMapToIntensities,vtkImageColocalizationTest,vtkImageColocalizationFilter,vtkImageAlphaFilter,vtkImageColorMerge}.{cxx,h}; do
    mv -f BioImageXD/vtkBXD/Processing/$f Imaging
    ln -sf Imaging/$f BioImageXD/vtkBXD/Processing
done

for f in  {vtkLSMReader,vtkExtTIFFReader}.{cxx,h}; do
    mv -f BioImageXD/vtkBXD/Processing/$f IO
    ln -sf IO/$f BioImageXD/vtkBXD/Processing
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
	-DVTK_USE_QT:BOOL=ON \
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

install -d -m 755 %{buildroot}/%{_datadir}/vtk
pushd %{buildroot}/%{_datadir}/vtk
    tar zxf %{SOURCE1}
    mv VTKData%{version}/{Baseline,Data} .
    rm -fr VTKData%{version}
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
rm -rf %{buildroot}/%{_libdir}/vtk/doc
rm -rf %{buildroot}/%{vtkdocdir}/verdict

# install test suite binaries and add each prg path in test-suite-files
rm -f test-suite-files
mkdir -p %{buildroot}%{_bindir}
pushd build/bin
    for f in `find . -type f | grep -v '.so$' | grep -v vtk`; do
	install -m 0755 $f %{buildroot}%{_bindir}
    done
popd

rm -f %{buildroot}%{_bindir}/*.so.*

%multiarch_includes  %{buildroot}%{vtkincdir}/vtkConfigure.h

#%multiarch_includes  %{buildroot}%{vtkincdir}/vtknetcdf/ncconfig.h

%changelog
* Wed Mar 14 2012 Paulo Andrade <pcpa@mandriva.com.br> 5.8.0-3
+ Revision: 784946
- Rebuild with current cooker packages.

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt against libtiff.so.5

* Wed Nov 16 2011 Paulo Andrade <pcpa@mandriva.com.br> 5.8.0-1
+ Revision: 731097
- Update to latest upstream release version 5.8.0

  + Oden Eriksson <oeriksson@mandriva.com>
    - attempt to relink against libpng15.so.15

* Wed May 11 2011 Funda Wang <fwang@mandriva.org> 5.6.1-3
+ Revision: 673642
- add soversion into vtkNetCDF_cxx also

* Sat May 07 2011 Funda Wang <fwang@mandriva.org> 5.6.1-2
+ Revision: 672272
- cosmo and vpic have so version now

* Sat May 07 2011 Funda Wang <fwang@mandriva.org> 5.6.1-1
+ Revision: 672221
- fix multiarch usage
- new version 5.6.1

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Thu Feb 03 2011 Funda Wang <fwang@mandriva.org> 5.6.0-4
+ Revision: 635603
- rebuild
- tighten BR

* Wed Nov 03 2010 Funda Wang <fwang@mandriva.org> 5.6.0-3mdv2011.0
+ Revision: 592774
- recognize py 2.7
- rebuild for py2.7

* Tue Aug 17 2010 Paulo Andrade <pcpa@mandriva.com.br> 5.6.0-2mdv2011.0
+ Revision: 570694
+ rebuild (emptylog)

* Thu Jul 15 2010 Paulo Andrade <pcpa@mandriva.com.br> 5.6.0-1mdv2011.0
+ Revision: 553766
- Correct problems with qt4 support
- Correct linkage of BioImageXD classes.
- Update to version 5.6.0.

* Wed Feb 10 2010 Paulo Andrade <pcpa@mandriva.com.br> 5.4.2-7mdv2010.1
+ Revision: 503996
- Rebuild with boost 1.42.0
- Correct broken symbolic links in devel package

* Mon Jan 11 2010 Funda Wang <fwang@mandriva.org> 5.4.2-6mdv2010.1
+ Revision: 489717
- disable proj as it locates in contrib
- use system proj

  + Oden Eriksson <oeriksson@mandriva.com>
    - fix br deps (python)
    - rebuilt against libjpeg v8

* Thu Sep 03 2009 Helio Chissini de Castro <helio@mandriva.com> 5.4.2-5mdv2010.0
+ Revision: 428698
- Fix .cmake files origin generation due to absolute/relative path and / strip on install code.
  Now vtk is installed officially in /usr except for his cmake modules, which are now installed in _libdir/vtk.
  With documentation in a separated package, vtk can be moved to main to help further requires libraries without a major hussle

* Thu Sep 03 2009 Helio Chissini de Castro <helio@mandriva.com> 5.4.2-4mdv2010.0
+ Revision: 428112
- Overhaul of old vtk package. Now vtk is properly installed in 64 and 32 bits following the libdir spec.
- Documentation are removed and will be added from the official tarball in a different package

* Sun Aug 23 2009 Funda Wang <fwang@mandriva.org> 5.4.2-2mdv2010.0
+ Revision: 419762
- rebuild for new libjpeg v7

  + Gaëtan Lehmann <glehmann@mandriva.org>
    - 5.4.2

* Mon May 04 2009 Funda Wang <fwang@mandriva.org> 5.2.1-2mdv2010.0
+ Revision: 371800
- add requires on libqt

* Tue Mar 17 2009 Gustavo De Nardin <gustavodn@mandriva.com> 5.2.1-1mdv2009.1
+ Revision: 356481
- disabled Java bindings, they're failing the build

  + Paulo Andrade <pcpa@mandriva.com.br>
    - Update to latest upstream release 5.2.1.
      o Update to use python 2.6.
      o Build java interface by default.
      o Move test-suite binaries to /usr/share/vtk/bin
      o Update BioImageXD to latest svn checkout (there are no official
      releases, but it is a mandatory component).
      o Added vtkdata component (and related upstream tarball).

  + Funda Wang <fwang@mandriva.org>
    - add 5.2.0 tarball

  + Adam Williamson <awilliamson@mandriva.org>
    - rebuild with python 2.6

* Mon Sep 29 2008 Funda Wang <fwang@mandriva.org> 5.0.3-4mdv2009.0
+ Revision: 289295
- finally fix filelist
- BR qt4
- fix underlink
- recognize python 2.5
- correct qtplugin dir

* Tue Sep 23 2008 Gaëtan Lehmann <glehmann@mandriva.org> 5.0.3-3mdv2009.0
+ Revision: 287206
- * fix build with gcc 4.3
  * fix build with python 2.4 installed
  * fix wrong location of qt lib
- fix wrong version required by the test-suite subpackage

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Sep 07 2007 Anssi Hannula <anssi@mandriva.org> 5.0.3-2mdv2008.0
+ Revision: 82036
- rebuild for new soname of tcl

* Sun Aug 26 2007 Gaëtan Lehmann <glehmann@mandriva.org> 5.0.3-1mdv2008.0
+ Revision: 71479
- drop wrong files
- 5.0.3
- fix build with tcl 8.5

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - rebuild for expat
    - some minor changes


* Fri Dec 22 2006 Gaëtan Lehmann <glehmann@mandriva.org> 5.0.2-3mdv2007.0
+ Revision: 101837
- fix loading of libvtkRenderingPythonTkWidgets when python-vtk-devel is not installed (bug #27340)

* Sat Dec 16 2006 Gaëtan Lehmann <glehmann@mandriva.org> 5.0.2-2mdv2007.1
+ Revision: 98187
- try to fix rebuild with iurt
- 5.0.2
- use RPM_OPT_FLAGS instead of Release mode
- Import vtk

  + Nicolas Lécureuil <neoclust@mandriva.org>
    - Rebuild against new python

  + Emmanuel Andry <eandry@mandriva.org>
    - bump release
      rebuild with python-2.5
      bunzipped patches

* Tue Jul 18 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.1-1mdv2007.0
- New release 5.0.1
- drop patch 1 (included in new release)

* Thu Jul 06 2006 Thierry Vignaud <tvignaud@mandriva.com> 5.0.0-12mdv2007.0
- fix group

* Wed Jul 05 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.0-11mdv2007.0
- rebuild to fix devel(libpng) dep

* Sun Jun 11 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.0-10mdv2007.0
- add extra classes from BioImageXD project

* Sun May 28 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.0-9mdv2007.0
- rebuild by hand

* Tue May 09 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.0-8mdk
- force QT_INCLUDE_DIR and QT_QT_LIBRARY (not detected when the package is
  built with iurt on x86_64)

* Tue Apr 18 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.0-7mdk
- examples requires vtk-data 5.0.0 (not 5.0)
- add {python,tcl}-vtk-devel packages to avoid devel(lib*) deps on those
  packages

* Wed Apr 12 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.0-6mdk
- build requires qt3-devel

* Sat Mar 25 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.0-5mdk
- build with Parallel option
- use sytem freetype

* Tue Mar 21 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.0-4mdk
- add qt package and clean the spec file (thanks to Joaquim Rodriguez
i Guerrero)
- update patch 1
- Patch2: fix wrong include

* Sat Mar 04 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.0-3mdk
- force /usr/bin/c++ compiler
- drop vtk symlink
- fix some lib path in config file on x86_64

* Fri Mar 03 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.0-2mdk
- Patch1: update to current 5.0.0 branch

* Wed Feb 01 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.0-1mdk
- 5.0.0

* Sun Jan 15 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.0-0.20051206.10mdk
- fix path in VTKConfig.cmake on 64 bits systems

* Thu Jan 12 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.0-0.20051206.9mdk
- fix Patch0

* Tue Jan 10 2006 Gaetan Lehmann <glehmann@n4.mandriva.com> 5.0.0-0.20051206.8mdk
- don't require tcl-devel and tk-devel for 2006.0 and previous releases

* Tue Jan 03 2006 Oden Eriksson <oeriksson@mandriva.com> 5.0.0-0.20051206.7mdk
- rebuilt against soname aware deps (tcl/tk)
- fix deps

* Tue Dec 20 2005 Gaetan Lehmann <glehmann@deborah.mandriva.com> 5.0.0-0.20051206.6mdk
- add vtk-5.0 -> vtk lik in lib dir for backward compatibility
- patch0: fix python qt widget

* Mon Dec 12 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.0-0.20051206.5mdk
- fix Requires devel(libtcl8.4) (thanks to Olivier Thauvin)
- drop patented switch (no more part of vtk)
- remove CVS dirs
- build requires tcl and tk

* Sun Dec 11 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.0-0.20051206.4mdk
- fix multiarch support

* Sun Dec 11 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.0-0.20051206.3mdk
- multiarch support

* Sat Dec 10 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 5.0.0-0.20051206.2mdk
- .so files in devel package

* Tue Dec 06 2005 Gaetan Lehmann <glehmann@deborah.mandriva.com> 5.0.0-0.20051206.1mdk
- vtk 5.0.0 cvs

* Fri Jun 10 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 4.4.2-7mdk
- make it build on x86_64

* Fri Apr 01 2005 Olivier Thauvin <nanardon@mandrake.org> 4.4.2-6mdk
- fix %%mkrel
- split data into another spec

* Fri Apr 01 2005 Olivier Thauvin <nanardon@mandrake.org> 4.4.2-5mdk
- use macro for few path, ensure spec will not going outside /home/mandrake/rpm/tmp/vtk-root
- %%mkrel

* Thu Mar 24 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 4.4.2-4mdk
- Use mkrel
- add "--with patented" switch

* Fri Mar 04 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 4.4.2-3mdk
- BuildRequires cmake >= 1.8 (thanks to Marc Koschewski)

* Thu Feb 17 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 4.4.2-2mdk
- fix data path for c++ and tcl examples
- fix vtk python lib dir
- add ldconfig call for libvtk package
- vtk-test-suite package is back

* Wed Feb 09 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 4.4.2-1mdk
- 4.4.2
- remove conditionnal doc build
- use more consistent names
- files attributes cleanup
- fix data path for python testing
- fix import patented exception

* Sun Jan 09 2005 Austin Acton <austin@mandrake.org> 4.2.6-1mdk
- fix some lint
- from Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> :
  - 4.2.6
  - add ld.so.conf path
  - fix python data path
  - compile python modules
  - add docs package
  - use system libs
  - fix JAVA_AWT_INCLUDE_PATH
  - USE_ANSI_STDLIB
  - add url to sources (to be able to update with rpmbuildupdate)
  - remove most of rpmlint warnings and errors
  - add version requirement to subpackages

* Sun Dec 05 2004 Michael Scherer <misc@mandrake.org> 4.2.2-6mdk	
- Rebuild for new python

* Wed Jun 30 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.2.2-5mdk
- rebuild for new g++
- patch 0: fix compiling with new g++

* Mon Mar 01 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 4.2.2-4mdk
- Own dir (again)

* Sun Feb 29 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 4.2.2-3mdk
- Own dir

