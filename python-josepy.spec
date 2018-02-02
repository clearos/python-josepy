%global pypi_name josepy

%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

Name:           python-%{pypi_name}
Version:        1.0.1
Release:        1%{?dist}
Summary:        JOSE protocol implementation in Python

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/josepy
Source0:        https://files.pythonhosted.org/packages/source/j/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%if 0%{?rhel} && 0%{?rhel} <= 7
Patch0:         allow-old-setuptools.patch
%endif

BuildRequires:  python2-devel
%if 0%{?rhel} && 0%{?rhel} <= 7
# EL7 has an unversioned name for this package
BuildRequires:  python-setuptools
%else
BuildRequires:  python2-setuptools
BuildRequires:  python2-sphinx
BuildRequires:  python2-sphinx_rtd_theme
%endif

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
JOSE protocol implementation in Python using cryptography.

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires:       python2-cryptography
BuildRequires:  python2-cryptography
%if 0%{?rhel} && 0%{?rhel} <= 7
# EL7 has unversioned names for these packages
Requires:       pyOpenSSL
Requires:       python-setuptools
Requires:       python-six
BuildRequires:  pyOpenSSL
BuildRequires:  python-setuptools
BuildRequires:  python-six
%else
Requires:       python2-pyOpenSSL
Requires:       python2-setuptools
Requires:       python2-six
BuildRequires:  python2-pyOpenSSL
BuildRequires:  python2-setuptools
BuildRequires:  python2-six
%endif

%description -n python2-%{pypi_name}
JOSE protocol implementation in Python using cryptography.

This is the Python 2 version of the package.

%if %{with python3}
%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3-cryptography
Requires:       python3-pyOpenSSL
Requires:       python3-setuptools
Requires:       python3-six
BuildRequires:  python3-cryptography
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-setuptools
BuildRequires:  python3-six

%description -n python3-%{pypi_name}
JOSE protocol implementation in Python using cryptography.

This is the Python 3 version of the package.

%endif

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if %{with python3}
%py3_build
%endif

# Build documentation
%if 0%{?fedora}
# EL7 has problems building the documentation due to fontawesome-fonts-web only
# being available on x86_64
%{__python2} setup.py install --user
make -C docs man PATH=${HOME}/.local/bin:$PATH
%endif

%install
%py2_install
%if %{with python3}
%py3_install
%endif

%if 0%{?fedora}
install -pD -t %{buildroot}%{_mandir}/man1 docs/_build/man/*.1*
%endif

%check
# TODO: Package missing test dependencies and reenable tests
# %{__python2} setup.py test
# %if %{with python3}
# %{__python3} setup.py test
# %endif

%files -n python2-%{pypi_name}
%license LICENSE.txt
%doc README.rst
%{python2_sitelib}/josepy
%{python2_sitelib}/josepy-%{version}-py?.?.egg-info
%if ! %{with python3}
%{_bindir}/jws
%else
%exclude %{_mandir}/man1/jws.1*
%endif
%if 0%{?fedora}
%{_mandir}/man1/*
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/josepy
%{python3_sitelib}/josepy-%{version}-py?.?.egg-info
%{_bindir}/jws
%if 0%{?fedora}
%{_mandir}/man1/*
%endif
%endif

%changelog
* Thu Jan 18 2018 Eli Young <elyscape@gmail.com> - 1.0.1-1
- Initial package.
