# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
# SPDX-FileContributor: Yifan Xu <xuyifan@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%global crate_name regex-automata
%global full_version 0.1.5
%global pkgname regex-automata-0.1

Name:           rust-regex-automata-0.1
Version:        0.1.5
Release:        %autorelease
Summary:        Rust crate "regex-automata"
License:        Unlicense/MIT
URL:            https://github.com/BurntSushi/regex-automata
#!RemoteAsset:  sha256:4324c97bd13d1f83985e92e805e4b5ca6d058fcafb4ccfc5c0e388bebeadaafc
Source:         https://crates.io/api/v1/crates/%{crate_name}/%{full_version}/download#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildSystem:    rustcrates

BuildRequires:  rust-rpm-macros

Requires:       crate(byteorder-1.0) >= 1.2.7
Provides:       crate(regex-automata) = %{version}
Provides:       crate(%{pkgname})

%description
Source code for takopackized Rust crate "regex-automata"

%package     -n %{name}+regex-syntax
Summary:        Automata construction and matching using regular expressions - feature "regex-syntax"
Requires:       crate(%{pkgname})
Requires:       crate(regex-syntax-0.6/default) >= 0.6.4
Provides:       crate(%{pkgname}/regex-syntax)

%description -n %{name}+regex-syntax
This metapackage enables feature "regex-syntax" for the Rust regex-automata crate, by pulling in any additional dependencies needed by that feature.

%package     -n %{name}+std
Summary:        Automata construction and matching using regular expressions - feature "std" and 1 more
Requires:       crate(%{pkgname})
Requires:       crate(%{pkgname}/regex-syntax)
Requires:       crate(%{pkgname}/utf8-ranges)
Provides:       crate(%{pkgname}/default)
Provides:       crate(%{pkgname}/std)

%description -n %{name}+std
This metapackage enables feature "std" for the Rust regex-automata crate, by pulling in any additional dependencies needed by that feature.

Additionally, this package also provides the "default" feature.

%package     -n %{name}+utf8-ranges
Summary:        Automata construction and matching using regular expressions - feature "utf8-ranges"
Requires:       crate(%{pkgname})
Requires:       crate(utf8-ranges-1.0/default) >= 1.0.0
Provides:       crate(%{pkgname}/utf8-ranges)

%description -n %{name}+utf8-ranges
This metapackage enables feature "utf8-ranges" for the Rust regex-automata crate, by pulling in any additional dependencies needed by that feature.

%files
%{_datadir}/cargo/registry/%{crate_name}-%{version}/

%changelog
%autochangelog
