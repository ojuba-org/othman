%global owner ojuba-org

Name: othman
Version: 0.5
Release: 1%{?dist}
Summary: Electronic Quran Browser
Summary(ar): مصحف إلكتروني
License: WAQFv2
URL: http://ojuba.org
Source: https://github.com/%{owner}/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch: noarch
BuildRequires: python-devel
BuildRequires: ImageMagick
BuildRequires: intltool
BuildRequires: sqlite
Requires: islamic-menus
Requires: amiri-quran-fonts
Requires: sqlite
Requires: pygobject3 >= 3.0.2
Requires: python-othman

%description
Othman Electronic Quran Browser displays Quranic text in Othmani script style
as written under authority of Othman ibn Affan the companion of prophet Muhammad PBUH

Othman project features fast search, autoscrolling, copy Quranic text to clipboard.

%description -l ar
يؤمّن مصحف عثمان الإلكتروني مستعرضًا لنص القرءان الكريم
يالخط العثماني و الذي تم ضبطه في عهد صاحب رسول الله
صلّ الله عليه و سلّم ، الخليفة الثّالث عثمان بن عفان رضي
الله عنه .

يؤمّن مصحف عثمان الإلكتروني سرعة في البحث و التّسيير
التّلقائي و إمكانية نسخ النّص القرءاني .

%prep
%autosetup -n %{name}-%{version}

%build
make %{?_smp_mflags}

%install
%make_install




# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2017 Mosaab Alzoubi <moceap@hotmail.com> -->
<!--
EmailAddress: moceap@hotmail.com
SentUpstream: 2017-1-8
-->
<application>
  <id type="desktop">Othman.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <summary>Electronic Quran Browser</summary>
  <summary xml:lang="ar">مصحف إلكتروني</summary>
  <description>
    <p>
	Electronic Quran Browser
    </p>
  </description>
  <description xml:lang="ar">
    <p>
	مصحف إلكتروني.
    </p>
  </description>
  <url type="homepage">https://github.com/ojuba-org/%{name}</url>
  <screenshots>
    <screenshot type="default">http://ojuba.org/screenshots/%{name}.png</screenshot>
  </screenshots>
  <updatecontact>moceap@hotmail.com</updatecontact>
</application>
EOF




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
Summary: Quranic text python module
Summary(ar): وحدة بيثون للنّص القرءاني
License: WAQFv2
BuildArch: noarch
Requires: python

%description -n python-othman
A python module that provides access to Quranic text with a fast search index

%description -n python-othman -l ar
وحدة بيثون تقدّم وصولًا كاملًا للنّص القرءاني مع إمكانية البحث ضمن فهرسة سريعة

%files
%license COPYING waqf2-ar.pdf
%doc README README-ar.txt
%{_bindir}/othman-browser
%{python2_sitelib}/othman/gtkUi.p*
%{_datadir}/applications/*.desktop
%{_datadir}/locale/*/*/*.mo
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/appdata/%{name}.appdata.xml

%files -n python-othman
%license COPYING waqf2-ar.pdf
%doc README README-ar.txt
%dir %{python2_sitelib}/othman
%dir %{_datadir}/othman
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/othman/core.p*
%{python2_sitelib}/othman/*varuints.p*
%{python2_sitelib}/othman/__init__.p*
%{_datadir}/othman/*

%changelog
* Sun Jan 8 2017 Mosaab Alzoubi <moceap@hotmail.com> - 0.5-1
- Update to 0.5
- New way to get Github upstream
- Add appdata

* Sat Nov 26 2016 Mosaab Alzoubi <moceap@hotmail.com> - 0.4-4
- Rebuilt for Fedora 25
- Add sqlite as BR and require

* Thu Jul 23 2015 Mosaab Alzoubi <moceap@hotmail.com> - 0.4-3
- Fix typo

* Thu Jul 16 2015 Mosaab Alzoubi <moceap@hotmail.com> - 0.4-2
- General clean
- Add Arabic summary and description
- Remove group tag
- Reset BRs
- Use %%make_install
- Modified description
- Remove old attr way
- Use %%license macro

* Mon Sep 29 2014 Mosaab Alzoubi <moceap@hotmail.com> - 0.4-1
- Update to 0.4.

* Tue Apr 8 2014 Mosaab Alzoubi <moceap@hotmail.com> - 0.3-3
- Fix requires.

* Mon Mar 24 2014 Ehab El-Gedawy <ehabsas@gmail.com> - 0.3-2
- change to amiri font

* Wed Mar 19 2014 Mosaab Alzoubi <moceap@hotmail.com> - 0.3-1
- New Relese

* Mon Jun 4 2012 Mosaab Alzoubi <moceap@hotmail.com> - 0.2.8-2
- General Revision.

* Mon Jun 4 2012  Muayyad Saleh AlSadi <alsadi@ojuba.org> - 0.2.8-1
- port to gtk3

* Sat Jun 12 2010  Muayyad Saleh AlSadi <alsadi@ojuba.org> - 0.2.5-1
- update to new version

* Wed Apr 28 2010 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 0.2.0-1
- initial release
