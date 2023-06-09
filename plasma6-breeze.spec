%define major %(echo %{version} |cut -d. -f1-3)
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)
%define git 20230707

Name: plasma6-breeze
Version:	5.240.0
Release:	%{?git:0.%{git}.}1
%if 0%{?git:1}
Source0:	https://invent.kde.org/plasma/breeze/-/archive/master/breeze-master.tar.bz2#/breeze-%{git}.tar.bz2
%else
Source0: http://download.kde.org/%{stable}/plasma/%{major}/%{name}-%{version}.tar.xz
%endif
Summary: The KDE 6 Breeze style
URL: http://kde.org/
License: GPL
Group: Graphical desktop/KDE
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: pkgconfig(xcb)
BuildRequires: cmake(KF6DocTools)
BuildRequires: cmake(Gettext)
BuildRequires: cmake(ECM)
BuildRequires: cmake(KDecoration2) >= 5.27.80
BuildRequires: cmake(KF6WindowSystem)
BuildRequires: cmake(KF6Service)
BuildRequires: cmake(KF6ConfigWidgets)
BuildRequires: cmake(KF6FrameworkIntegration)
BuildRequires: cmake(KF6KCMUtils)
BuildRequires: cmake(KF6Plasma)
BuildRequires: cmake(KF6Wayland)
BuildRequires: cmake(KF6Kirigami2)
BuildRequires: pkgconfig(fftw3)
# Just to prevent Plasma 5 from being pulled in
BuildRequires: plasma6-xdg-desktop-portal-kde

%description
The KDE 6 Breeze style.

%package devel
Summary: Devel stuff for %{name}
Group: Development/KDE and Qt
Requires: %{name} = %{EVRD}
Provides: %{name}-devel = %{EVRD}

%description devel
This package contains header files needed if you wish to build applications
based on %{name}.

%prep
%autosetup -p1 -n breeze-%{?git:master}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

%find_lang breeze_style_config || touch breeze_style_config.lang
%find_lang breeze_kwin_deco || touch breeze_kwin_deco.lang
cat  *.lang >all.lang

%files -f all.lang
%{_bindir}/breeze-settings6
%{_libdir}/libbreezecommon6.so*
%{_datadir}/kconf_update/breezetobreezelight.upd
%{_datadir}/icons/breeze_cursors
%{_datadir}/icons/Breeze_Light
%{_datadir}/wallpapers/*
%{_datadir}/kstyle/themes/breeze.themerc
%{_libdir}/kconf_update_bin/breezetobreezelight
%{_datadir}/QtCurve
%{_datadir}/color-schemes/BreezeDark.colors
%{_datadir}/color-schemes/BreezeLight.colors
%{_qtdir}/plugins/styles/breeze.so
%{_qtdir}/plugins/org.kde.kdecoration2/*.so
%{_iconsdir}/hicolor/scalable/apps/breeze-settings.svgz
%{_libdir}/kconf_update_bin/breezehighcontrasttobreezedark
%{_libdir}/kconf_update_bin/breezetobreezeclassic
%{_datadir}/color-schemes/BreezeClassic.colors
%{_datadir}/kconf_update/breezehighcontrasttobreezedark.upd
%{_datadir}/kconf_update/breezetobreezeclassic.upd
%{_qtdir}/plugins/plasma/kcms/systemsettings_qwidgets/breezestyleconfig.so
%{_datadir}/applications/breezestyleconfig.desktop
%{_datadir}/applications/kcm_breezedecoration.desktop
%dir %{_qtdir}/plugins/org.kde.kdecoration2.kcm
%{_qtdir}/plugins/org.kde.kdecoration2.kcm/kcm_breezedecoration.so

%files devel
%{_libdir}/cmake/Breeze
