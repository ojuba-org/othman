Name:		othman
Version:	0.6.0
Release:	1%{?dist}
Summary:	Othman Electronic Quran Browser

Group:		Applications/Productivity
License:	Waqf
URL:		http://othman.ojuba.org
Source:		http://git.ojuba.org/cgit/%{name}/snapshot/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:	python3
BuildRequires: intltool

Requires:	islamic-menus, arabeyes-core-fonts
Requires:	python3-gobject
Requires:	python-othman

%description
Othman Electronic Quran Browser displays Quranic text in Othmani script style
as written under authority of Othman ibn Affan the companion of prophet Muhammad PBUH

Othman project features fast search, autoscrolling, copy Quranic text to clipboard.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
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

%clean
rm -rf $RPM_BUILD_ROOT

%package -n python-othman
Group:		System Environment/Base
Summary:	python package providing access to Quranic text
License:	Waqf
BuildArch:	noarch
Requires:	python
%description -n python-othman
a python package that provides access to Quranic text with a fast search index

%files
%defattr(-,root,root,-)
%doc LICENSE-en LICENSE-ar.txt README README-ar.txt COPYING
%{_bindir}/othman-browser
%{python3_sitelib}/othman/gtkUi.p*
%{_datadir}/applications/*.desktop
%{_datadir}/locale/*/*/*.mo
%{_datadir}/icons/hicolor/*/apps/*.png

%files -n python-othman
%defattr(-,root,root,-)
%doc LICENSE-en LICENSE-ar.txt README README-ar.txt COPYING
%dir %{python3_sitelib}/othman
%dir %{_datadir}/othman
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/othman/core.p*
%{python3_sitelib}/othman/univaruints.p*
%{python3_sitelib}/othman/__init__.p*
%{python3_sitelib}/othman//__pycache__/*.pyc
%{_datadir}/othman/*

%changelog
* Sat Sep 28 2019  Muayyad Saleh AlSadi <alsadi@ojuba.org> - 0.6.0-1
- python3

* Mon Jun 4 2012  Muayyad Saleh AlSadi <alsadi@ojuba.org> - 0.2.8-1
- port to gtk3

* Sat Jun 12 2010  Muayyad Saleh AlSadi <alsadi@ojuba.org> - 0.2.5-1
- update to new version

* Wed Apr 28 2010 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 0.2.0-1
- initial release

