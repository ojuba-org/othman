%global owner ojuba-org
%global commit #Write commit number here

Name:		othman
Version:	0.2.8
Release:	2%{?dist}
Summary:	Othman Electronic Quran Browser
Group:		Applications/Productivity
License:	WAQFv2
URL:		http://ojuba.org
Source:		https://github.com/%{owner}/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	python2-devel
Requires:	islamic-menus
Requires:	arabeyes-core-fonts
Requires:	pygobject3 >= 3.0.2
Requires:	python-othman

%description
Othman Electronic Quran Browser displays Quranic text in Othmani script style
as written under authority of Othman ibn Affan the companion of prophet Muhammad PBUH

Othman project features fast search, autoscrolling, copy Quranic text to clipboard.

%prep
%setup -q -n %{name}-%{commit}

%build
make %{?_smp_mflags}

%install
%makeinstall DESTDIR=$RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%package -n python-othman
Group:		System Environment/Base
Summary:	python package providing access to Quranic text
License:	WAQFv2
BuildArch:	noarch
Requires:	python

%description -n python-othman
a python package that provides access to Quranic text with a fast search index

%files
%defattr(-,root,root,-)
%doc README README-ar.txt COPYING waqf2-ar.pdf
%{_bindir}/othman-browser
%{python2_sitelib}/othman/gtkUi.p*
%{_datadir}/applications/*.desktop
%{_datadir}/locale/*/*/*.mo
%{_datadir}/icons/hicolor/*/apps/*.png

%files -n python-othman
%defattr(-,root,root,-)
%doc README README-ar.txt COPYING waqf2-ar.pdf
%dir %{python2_sitelib}/othman
%dir %{_datadir}/othman
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/othman/core.p*
%{python2_sitelib}/othman/*varuints.p*
%{python2_sitelib}/othman/__init__.p*
%{_datadir}/othman/*

%changelog
* Mon Jun 4 2012 Mosaab Alzoubi <moceap@hotmail.com> - 0.2.8-2
- General Revision.

* Mon Jun 4 2012  Muayyad Saleh AlSadi <alsadi@ojuba.org> - 0.2.8-1
- port to gtk3

* Sat Jun 12 2010  Muayyad Saleh AlSadi <alsadi@ojuba.org> - 0.2.5-1
- update to new version

* Wed Apr 28 2010 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 0.2.0-1
- initial release
