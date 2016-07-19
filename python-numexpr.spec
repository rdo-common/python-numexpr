%global with_python3 1

# we don't want to provide private python extension libs in either the python2 or python3 dirs
%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/.*\\.so$

%global module numexpr

Summary:        Fast numerical array expression evaluator for Python and NumPy
Name:           python-%{module}
Version:        2.6.1
Release:        2%{?dist}
Source0:        https://github.com/pydata/numexpr/archive/v%{version}.tar.gz#/%{module}-%{version}.tar.gz
License:        MIT
Group:          Development/Languages
URL:            https://github.com/pydata/numexpr

BuildRequires:  numpy >= 1.6
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-numpy
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif # with_python3

%global _description \
The numexpr package evaluates multiple-operator array expressions many \
times faster than NumPy can. It accepts the expression as a string,    \
analyzes it, rewrites it more efficiently, and compiles it to faster   \
Python code on the fly. It’s the next best thing to writing the        \
expression in C and compiling it with a specialized just-in-time (JIT) \
compiler, i.e. it does not require a compiler at runtime.

%description %_description

%package -n python2-%{module}
Summary:        %{summary}
Requires:       numpy >= 1.6
%{?python_provide:%python_provide python2-%{module}}

%description -n python2-%{module} %_description

This is the version for Python 2.

%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-%{module}
Summary:        %{summary}
Requires:       python%{python3_pkgversion}-numpy >= 1.6
%{?python_provide:%python_provide python%{python3_pkgversion}-%{module}}

%description -n python%{python3_pkgversion}-%{module} %_description

This is the version for Python 3.
%endif # with_python3


%prep
%setup -q -n %{module}-%{version}

sed -i "s|/usr/bin/env |/usr/bin/|" %{module}/cpuinfo.py

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif # with_python3

%install
%py2_install
#This could be done more properly ?
chmod 0755 %{buildroot}%{python_sitearch}/%{module}/cpuinfo.py
chmod 0644 %{buildroot}%{python_sitearch}/%{module}/*.so
%if 0%{?with_python3}
%py3_install
chmod 0755 %{buildroot}%{python3_sitearch}/%{module}/cpuinfo.py
%endif # with_python3

%check
pushd build/lib.linux*%{python2_version}
%{__python2} -c 'import numexpr; numexpr.test()'
popd
%if 0%{?with_python3}
pushd build/lib.linux*%{python3_version}
PYTHONPATH=%{buildroot}%{python3_sitearch} %{__python3} -c 'import numexpr; numexpr.test()'
popd
%endif # with_python3

%files -n python2-%{module}
%license LICENSE.txt
%doc ANNOUNCE.rst RELEASE_NOTES.rst README.rst
%{python2_sitearch}/numexpr/
%{python2_sitearch}/numexpr-%{version}-py*.egg-info/

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{module}
%license LICENSE.txt
%doc ANNOUNCE.rst RELEASE_NOTES.rst README.rst
%{python3_sitearch}/numexpr/
%{python3_sitearch}/numexpr-%{version}-py*.egg-info
%endif # with_python3

%changelog
* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jul 19 2016 Thibault North <tnorth@fedoraproject.org> - 2.6.1-1
- Update to 2.6.1
- Fix project URL
- Fix cpuinfo permission in py3 package

* Wed Jun  1 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6.0-1
- Update to latest version

* Tue May 17 2016 Orion Poplawski <orion@cora.nwra.com> - 2.5.2-2
- Update provides filter
- Use %%python3_pkgversion for EPEL7 compatibility
- Drop %%py3dir

* Tue Apr 12 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.5.2-1
- Update to latest version (#1305251)

* Sat Feb  6 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.5-1
- Update to latest version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 18 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4.6-2
- Create python2 subpackage

* Sat Nov 14 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4.6-1
- Update to latest version

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.3-5
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Jan 28 2014 Thibault North <tnorth@fedoraproject.org> -2.3-1
- Update to new release 2.3

* Fri Jan 17 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.2.2-2
- Move requirements to the proper package (#1054683)

* Sun Sep 29 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.2.2-1
- Update to 2.2.2 (#1013130)

* Mon Sep 09 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.2.1-1
- Update to 2.2.1

* Thu Sep 05 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.2-1
- Update to 2.2
- Add python3-numexpr package

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 8 2012  Thibault North <tnorth@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1

* Sun Nov 27 2011 Thibault North <tnorth@fedoraproject.org> - 2.0-1
- Update to 2.0

* Sun Oct 30 2011 Thibault North <tnorth@fedoraproject.org> - 1.4.2-2
- Add check section
- Fix permissions and remove useless sections

* Thu Oct 20 2011 Thibault North <tnorth@fedoraproject.org> - 1.4.2-1
- Updated to 1.4.2

* Fri Apr 29 2011 Thibault North <tnorth@fedoraproject.org> - 1.4.1-3
- Fix buildroot issue

* Tue Dec 21 2010 Thibault North <tnorth@fedoraproject.org> - 1.4.1-2
- Fixes for the review process

* Fri Nov 05 2010 Thibault North <tnorth@fedoraproject.org> - 1.4.1-1
- Initial package based on Mandriva's one
