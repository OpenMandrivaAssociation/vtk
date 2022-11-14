#!/bin/sh
git ls-remote --tags https://gitlab.kitware.com/vtk/vtk.git 2>/dev/null |awk '{ print $2; }'  |grep -v '\^{}' |sed -e 's,refs/tags/v,,' |sort -V |tail -n1
