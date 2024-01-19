Vendor:         Microsoft Corporation
Distribution:   Mariner

%bcond check 1

# Enable all tests (requires check to be true)
%bcond all_tests 0

Name:          python-argcomplete
Summary:       Bash tab completion for argparse
Version:       3.2.1
Release:       2%{?dist}
License:       Apache-2.0
URL:           https://github.com/kislyuk/argcomplete
Source0:       %pypi_source argcomplete

BuildRequires: python3-devel

%if %{with check}
BuildRequires: tcsh
BuildRequires: fish
BuildRequires: zsh
%endif

BuildArch:     noarch

%global _description %{expand:
Tab complete all the things!

Argcomplete provides easy, extensible command line tab completion of
arguments for your Python application.

It makes two assumptions:

 - You're using bash or zsh as your shell
 - You're using argparse to manage your command line arguments/options
 
Argcomplete is particularly useful if your program has lots of options
or subparsers, and if your program can dynamically suggest completions
for your argument/option values (for example, if the user is browsing
resources over the network).}

%description %_description

%package -n python3-argcomplete
Summary:        %{summary}
%description -n python3-argcomplete %_description

%prep
%autosetup -p1 -n argcomplete-%{version}
# Remove useless BRs (aka linters)
sed -i -r -e '/test = /s/"(coverage|ruff|mypy)"[, ]*//g' pyproject.toml

# https://github.com/kislyuk/argcomplete/issues/255
# https://github.com/kislyuk/argcomplete/issues/256
sed -i -e "1s|#!.*python.*|#!%{__python3}|" test/prog scripts/*
sed -i -e "s|python |python3 |" test/test.py

%generate_buildrequires
%pyproject_buildrequires %{?with_check:-x test}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files argcomplete


# do not attempt to install to %%bash_completions_dir, see https://bugzilla.redhat.com/2211862
install -Dp -m0644 argcomplete/bash_completion.d/_%{name} %{buildroot}%{_sysconfdir}/bash_completion.d/_%{name}

%if %{with check}
%check
%if %{with all_tests}
%{py3_test_envvars} %{python3} test/test.py -v
%else
# Disable zsh tests. They fail for mysterious reasons.
# https://github.com/kislyuk/argcomplete/issues/447
%{py3_test_envvars} %{python3} test/test.py -v -k "TestArgcomplete"
%{py3_test_envvars} %{python3} test/test.py -v -k "TestBash"
%{py3_test_envvars} %{python3} test/test.py -v -k "TestCheckModule"
%{py3_test_envvars} %{python3} test/test.py -v -k "TestSplitLine"
%endif
%endif

%files -n python3-argcomplete -f %{pyproject_files}
%license LICENSE.rst
%doc README.rst
%{_bindir}/activate-global-python-argcomplete
%{_bindir}/python-argcomplete-check-easy-install-script
%{_bindir}/register-python-argcomplete
%{_sysconfdir}/bash_completion.d/_%{name}

%changelog
* Tue Jan 16 17:26:11 EST 2024 Dan Streetman <ddstreet@ieee.org> - 3.2.1-2
- Update to version from Fedora 39/rawhide.
- Next line is present only to avoid tooling failures, and does not indicate the actual package license.
- Initial CBL-Mariner import from Fedora 39 (license: MIT).
- license verified

# We can't use autochangelog unfortunately
#autochangelog
