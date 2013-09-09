%global with_python3 1

%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_provides_in %{python3_sitearch}/.*\.so$
%filter_setup}

%global	module	numexpr

Summary:	Fast numerical array expression evaluator for Python and NumPy
Name:		python-%{module}
Version:	2.2.1
Release:	1%{?dist}
Source0:	http://numexpr.googlecode.com/files/%{module}-%{version}.tar.gz
License:	MIT
Group:		Development/Languages
URL:		http://numexpr.googlecode.com/

Requires:	numpy >= 1.6
BuildRequires:	numpy >= 1.6
BuildRequires:	python2-devel
%if 0%{?with_python3}
Requires:	python3-numpy >= 1.6
BuildRequires:	python3-devel
BuildRequires:  python3-numpy
%endif # with_python3

%description
The numexpr package evaluates multiple-operator array expressions many
times faster than NumPy can. It accepts the expression as a string,
analyzes it, rewrites it more efficiently, and compiles it to faster
Python code on the fly. It's the next best thing to writing the
expression in C and compiling it with a specialized just-in-time (JIT)
compiler, i.e. it does not require a compiler at runtime.

%if 0%{?with_python3}
%package -n python3-%{module}
Summary:	Fast numerical array expression evaluator for Python and NumPy

%description -n python3-%{module}
The numexpr package evaluates multiple-operator array expressions many
times faster than NumPy can. It accepts the expression as a string,
analyzes it, rewrites it more efficiently, and compiles it to faster
Python code on the fly. It's the next best thing to writing the
expression in C and compiling it with a specialized just-in-time (JIT)
compiler, i.e. it does not require a compiler at runtime.

This is the version for Python 3.
%endif # with_python3


%prep
%setup -q -n %{module}-%{version}

sed -i "s|/usr/bin/env |/usr/bin/|" %{module}/cpuinfo.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
python setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
python3 setup.py build
popd
%endif # with_python3

%check
libdir=`ls build/|grep lib`
pushd "build/$libdir"
python -c 'import numexpr; numexpr.test()'
popd

%if 0%{?with_python3}
pushd %{py3dir}
libdir=`ls build/|grep lib`
cd "build/$libdir"
python3 -c 'import numexpr; numexpr.test()'
popd
%endif # with_python3

%install
python setup.py install -O1 --skip-build --root=%{buildroot}
#This could be done more properly ?
chmod 0644 %{buildroot}%{python_sitearch}/%{module}/cpuinfo.py
chmod 0755 %{buildroot}%{python_sitearch}/%{module}/*.so

%if 0%{?with_python3}
pushd %{py3dir}
python3 setup.py install -O1 --skip-build --root=%{buildroot}
popd
%endif # with_python3

%files
%doc ANNOUNCE.txt LICENSE.txt RELEASE_NOTES.txt README.txt
%{python_sitearch}/numexpr/
%{python_sitearch}/numexpr-%{version}-py*.egg-info/

%if 0%{?with_python3}
%files -n python3-%{module}
%doc ANNOUNCE.txt LICENSE.txt RELEASE_NOTES.txt README.txt
%{python3_sitearch}/numexpr/
%{python3_sitearch}/numexpr-%{version}-py*.egg-info
%endif # with_python3

%changelog
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
