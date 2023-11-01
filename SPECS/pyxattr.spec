%global with_python3 1

%if 0%{?rhel} > 7
# Disable python2 build by default
%global with_python2 0
%else
%global with_python2 1
%endif

Name:		pyxattr
Summary:	Extended attributes library wrapper for Python
Version:	0.5.3
Release:	18%{?dist}
License:	LGPLv2+
Group:		Development/Libraries
URL:		http://pyxattr.k1024.org/
Source:		https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
Patch0:		0001-use-Py_ssize_t.patch
Patch1:         0002-add-workaround-for-undefined-ENOATTR.patch
BuildRequires:	libattr-devel
%if %{?with_python2}
BuildRequires:	python2-devel, python2-setuptools
%endif
%if %{?with_python3}
BuildRequires:	python3-devel, python3-setuptools
%endif # with_python3

%global _description\
Python extension module wrapper for libattr. It allows to query, list,\
add and remove extended attributes from files and directories.

%description %_description

%if %{?with_python2}
%package -n python2-%{name}
Summary: %summary
%{?python_provide:%python_provide python2-%{name}}
# Remove before F30
Provides: pyxattr = %{version}-%{release}
Provides: pyxattr%{?_isa} = %{version}-%{release}
Obsoletes: pyxattr < %{version}-%{release}

%description -n python2-%{name} %_description
%endif

%if %{?with_python3}
%package -n python3-%{name}
Summary:	Extended attributes library wrapper for Python 3

%description -n python3-%{name}
Python extension module wrapper for libattr. It allows to query, list,
add and remove extended attributes from files and directories.

Python 3 version.
%endif # with_python3

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%if %{?with_python2}
CFLAGS="%{optflags}" %{__python2} setup.py build
%endif

%if 0%{?with_python3}
CFLAGS="%{optflags}" %{__python3} setup.py build
%endif # with_python3

%install
%if %{?with_python2}
%{__python2} setup.py install --root="%{buildroot}" --prefix="%{_prefix}"
%endif

%if 0%{?with_python3}
%{__python3} setup.py install --root="%{buildroot}" --prefix="%{_prefix}"
%endif # with_python3

%check
# selinux in koji produces unexpected xattrs for tests
export TEST_IGNORE_XATTRS=security.selinux

%if %{?with_python2}
%{__python2} setup.py test
%endif

%if 0%{?with_python3}
%{__python3} setup.py test
%endif # with_python3

%if %{?with_python2}
%files -n python2-%{name}
%defattr(0644,root,root,0755)
%{python2_sitearch}/xattr.so
%{python2_sitearch}/*egg-info
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README
%endif

%if %{?with_python3}
%files -n python3-%{name}
%defattr(0644,root,root,0755)
%{python3_sitearch}/xattr.cpython-??m*
%{python3_sitearch}/*egg-info
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README
%endif # with_python3

%changelog
* Sat Aug 04 2018 Milind Changire <mchangir@redhat.com> - 0.5.3-18
- fixes bz#1610029

* Tue Jun 26 2018 Lumír Balhar <lbalhar@redhat.com> - 0.5.3-17
- Python 2 subpackage disable by default

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.5.3-15
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Dec 26 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.3-14
- Also add Provides for the old name without %%_isa

* Sun Aug 13 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.3-13
- Python 2 binary package renamed to python2-pyxattr
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.5.3-9
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-8
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 0.5.3-6
- Rebuilt for Python3.5 rebuild
- Change pattern for listed so file to reflect new naming in py35

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug  7 2014 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.5.3-3
- add Mark Hamzy's patch to fix issue with PPC builds (bug 1127310)

* Mon Aug  4 2014 Tom Callaway <spot@fedoraproject.org> - 0.5.3-2
- fix license handling

* Sat Jun 28 2014 Miro Hrončok <mhroncok@redhat.com> - 0.5.3-1
- Updated to 0.5.3
- Updated the website
- Updated download URL to PyPI
- Removed useless Require of python >= 2.2
- Use %%{pythonX_sitearch} macros
- Removed BuildRoot definition, %%clean section and rm -rf at the beginning of %%install
- Introduced Python 3 subpackage
- Introduced %%check and run the test suite

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.5.1-1
- updated to 0.5.1
- fix bugs found with cpychecker (bug 809974)

* Mon Feb 27 2012 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.5.0-5
- remove prodive/obsolete of python-xattr (bug 781838)
- fix problem with mixed use of tabs and spaces

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Dec 27 2009 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.5.0-1
- updated to 0.5.0
- added support for unicode filenames (bug 479417)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 6 2008 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.4.0-2
- added python-setuptools in BuildRequires which is needed in build process
since version 0.4.0 (thanks to Kevin Fenzi)

* Fri Dec 5 2008 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.4.0-1
- updated to 0.4.0
- License Tag adjusted to current licensing LGPLv2+
- modified Python Eggs support due to its usage in source distribution 

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.2-4
- Rebuild for Python 2.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.2-3
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.2-2
- added compatibility with Python Eggs forced in F9 

* Mon Aug 27 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.2-1
- upgraded to 0.2.2

* Sun Aug 26 2007 Kevin Fenzi <kevin@tummy.com> - 0.2.1-5
 - Updated License tag

* Wed Apr 25 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.1-4
 - added Provides/Obsoletes tags

* Sat Apr 21 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.1-3
 - removed redundant after name change "exclude" tag
 - comments cleanup

* Wed Apr 18 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.1-2
 - applied suggestions from Kevin Fenzi
 - name changed from python-xattr to pyxattr
 - corrected path to the source file

* Thu Apr 5 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.1-1
 - updated to 0.2.1
 - added python-devel in BuildRequires
 - added more doc files
 - added Provides section
 - modified to Fedora Extras requirements

* Sun Sep 11 2005 Dag Wieers <dag@wieers.com> - 0.2-1 - +/
- Initial package. (using DAR)
