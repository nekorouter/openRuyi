# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: Yifan Xu <xuyifan@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%global srcname triton
%global _lto_cflags %{nil}
%global llvm_maj_ver 22

Name:           python-%{srcname}
Version:        3.7.0
Release:        %autorelease
Summary:        Language and compiler for custom deep-learning primitives
License:        MIT
URL:            https://triton-lang.org/main/index.html
VCS:            git:https://github.com/triton-lang/triton.git
#!RemoteAsset:  sha256:980397efada8ed2de303a95ad918e7454df13d7df5941840646e8004d4bd0462
Source0:        https://github.com/triton-lang/triton/releases/download/v%{version}/%{srcname}-%{version}.tar.gz
BuildSystem:    pyproject

BuildOption(install):  -l %{srcname}
BuildOption(check):  -e 'triton.instrumentation.*'
BuildOption(check):  -e 'triton.plugins.*'
BuildOption(check):  -e 'triton.runtime.interpreter'
BuildOption(check):  -e 'triton.tools.mxfp'

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  lld%{llvm_maj_ver}-devel
BuildRequires:  llvm%{llvm_maj_ver}-devel
BuildRequires:  llvm%{llvm_maj_ver}-static
BuildRequires:  mlir%{llvm_maj_ver}-devel
BuildRequires:  ninja
BuildRequires:  nlohmann-json
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(python3)
BuildRequires:  pkgconfig(pybind11)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3dist(build)
BuildRequires:  python3dist(installer)
BuildRequires:  python3dist(pybind11)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(wheel)

%patchlist
# Use system-provided build tools instead of vendored copies.
0001-use-system-build-tools.patch
# Adjust for the MLIR 22 C API.
0002-mlir-22-api.patch
# Link dynamically against the shared LLVM/MLIR libraries.
0003-link-dynamic-llvm.patch
# Disable the NVIDIA backend (not relevant for the RISC-V target).
0004-disable-nvidia-backend.patch

%description
Triton is a language and compiler for writing highly efficient custom
deep-learning primitives. It provides a Python programming interface and a
compiler stack that lowers Triton kernels through MLIR and LLVM backends for
GPU execution.

%generate_buildrequires
%pyproject_buildrequires

%build -p
export LLVM_CONFIG="%{_libdir}/llvm%{llvm_maj_ver}/bin/llvm-config-%{llvm_maj_ver}"
export LLVM_SYSPATH="%{_libdir}/llvm%{llvm_maj_ver}"
export PATH="%{_libdir}/llvm%{llvm_maj_ver}/bin:${PATH}"
export JSON_SYSPATH="%{_prefix}"
export PYBIND11_SYSPATH="%{_prefix}"
export PYBIND11_CMAKE_DIR="%{_datadir}/cmake/pybind11"
export TRITON_CODEGEN_BACKENDS=amd
export TRITON_BUILD_PROTON=OFF
export TRITON_APPEND_CMAKE_ARGS="-DTRITON_BUILD_EXAMPLES=OFF -DTRITON_BUILD_TOOLS=OFF -DLLVM_LINK_LLVM_DYLIB=ON -DMLIR_LINK_MLIR_DYLIB=ON -DCMAKE_BUILD_RPATH=%{_libdir}/llvm22/lib -DCMAKE_INSTALL_RPATH=%{_libdir}/llvm22/lib -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON"
export TRITON_OFFLINE_BUILD=1
export MAX_JOBS="${MAX_JOBS:-4}"
export CFLAGS="${CFLAGS} -fuse-ld=lld"
export CXXFLAGS="${CXXFLAGS} -fuse-ld=lld"
export LDFLAGS="${LDFLAGS} -fuse-ld=lld"

%files -f %{pyproject_files}
%doc README.md
%license LICENSE

%changelog
%autochangelog
