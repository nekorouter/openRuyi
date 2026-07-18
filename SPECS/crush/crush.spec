# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
# SPDX-FileContributor: openRuyi Packaging <packaging@openruyi.org>
#
# SPDX-License-Identifier: MulanPSL-2.0

%global go_import_path github.com/charmbracelet/crush

Name:           crush
Version:        0.85.0
Release:        %autorelease
Summary:        Terminal-based AI coding assistant with multi-model LLM support

License:        FSL-1.1-MIT
URL:            https://github.com/charmbracelet/crush
VCS:            git:https://github.com/charmbracelet/crush.git
#!RemoteAsset:  sha256:48b947c568562eaec6a0c3f8731cda4c3bd4eb1b2cc6d8a3c163f8726144393b
Source:         %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildSystem:    golang

BuildOption(prep):  -n %{name}-%{version}

BuildRequires:  go
BuildRequires:  go-rpm-macros

%description
Crush is a terminal-based AI coding assistant from Charm. It wires your tools,
code, and workflows into the LLM of your choice. It supports multi-model
sessions, LSP integration, MCP servers (http, stdio, sse), and works across
macOS, Linux, Windows, FreeBSD, OpenBSD, and NetBSD.

# Manual %build: crush uses Go modules (go.mod) with 100+ dependencies, so the
# GOPATH-mode %go_common macro does not fit. Build directly with go build in
# module mode (GO111MODULE=on) so dependencies resolve from go.sum.
%build
cd %{_builddir}/%{name}-%{version}
export GO111MODULE=on
export CGO_ENABLED=0
export GOFLAGS="-trimpath -mod=readonly -modcacherw"
go build \
    -ldflags "-s -w -X github.com/charmbracelet/crush/internal/version.Version=%{version}" \
    -o %{name} .

# Generate shell completions and man page with the just-built binary.
mkdir -p completions manpages
./%{name} completion bash > completions/%{name}.bash
./%{name} completion zsh  > completions/%{name}.zsh
./%{name} completion fish > completions/%{name}.fish
./%{name} man | gzip -c   > manpages/%{name}.1.gz

%install
install -d %{buildroot}%{_bindir}
install -m 0755 %{_builddir}/%{name}-%{version}/%{name} \
    %{buildroot}%{_bindir}/%{name}

install -d %{buildroot}%{bash_completions_dir}
install -m 0644 %{_builddir}/%{name}-%{version}/completions/%{name}.bash \
    %{buildroot}%{bash_completions_dir}/%{name}

install -d %{buildroot}%{_datadir}/zsh/site-functions
install -m 0644 %{_builddir}/%{name}-%{version}/completions/%{name}.zsh \
    %{buildroot}%{_datadir}/zsh/site-functions/_%{name}

install -d %{buildroot}%{_datadir}/fish/vendor_completions.d
install -m 0644 %{_builddir}/%{name}-%{version}/completions/%{name}.fish \
    %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish

install -d %{buildroot}%{_mandir}/man1
install -m 0644 %{_builddir}/%{name}-%{version}/manpages/%{name}.1.gz \
    %{buildroot}%{_mandir}/man1/%{name}.1.gz

%check
# Test suite requires network access for Go module downloads and live LLM
# API credentials for end-to-end tests; skipped in offline build.

%files
%doc README.md AGENTS.md
%license LICENSE.md
%{_bindir}/%{name}
%{bash_completions_dir}/%{name}
%{_datadir}/zsh/site-functions/_%{name}
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_mandir}/man1/%{name}.1.gz*

%changelog
%autochangelog
