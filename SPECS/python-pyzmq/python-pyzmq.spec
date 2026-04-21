# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: Yifan Xu <xuyifan@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%global srcname pyzmq

Name:           python-%{srcname}
Version:        27.1.0
Release:        %autorelease
Summary:        Python bindings for zeromq
License:        BSD-3-Clause AND LGPL-2.1-or-later AND Apache-2.0
URL:            https://github.com/zeromq/pyzmq
#!RemoteAsset
Source0:        https://files.pythonhosted.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz
BuildSystem:    pyproject

BuildOption(build):     %{shrink:
                        -Ccmake.define.PYZMQ_LIBZMQ_RPATH:BOOL=OFF
                        -Ccmake.define.PYZMQ_NO_BUNDLE=ON
                        -Clogging.level=INFO
                        -Cbuild.verbose=true
                        -Ccmake.build-type="RelWithDebInfo"}
BuildOption(install):  -L zmq
BuildOption(check):     %{shrink:
                        -e 'zmq.backend.cffi*'
                        %{?!with_gevent:-e 'zmq.green*'}
                        }

BuildRequires:  pyproject-rpm-macros
BuildRequires:  pkgconfig(python3)
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja
BuildRequires:  pkgconfig(libzmq)
BuildRequires:  python3-pysocks
BuildRequires:  python3-cffi
BuildRequires:  python3-tornado
BuildRequires:  python3-pytest

Provides:       python3-pyzmq
%python_provide python3-pyzmq

%description
This package contains Python bindings for ZeroMQ. ØMQ is a lightweight and fast
messaging implementation.

%generate_buildrequires
%pyproject_buildrequires

%files -f %{pyproject_files}
%doc README.md
%license LICENSE.md licenses/

%changelog
%{?autochangelog}
