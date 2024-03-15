%define major %(echo %{version} |cut -d. -f1-3)
%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)
#define git 20240222
%define gitbranch Plasma/6.0
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")

%bcond_without qt5

Name: plasma6-breeze
Version:	6.0.2
Release:	%{?git:0.%{git}.}2
%if 0%{?git:1}
Source0:	https://invent.kde.org/plasma/breeze/-/archive/%{gitbranch}/breeze-%{gitbranchd}.tar.bz2#/breeze-%{git}.tar.bz2
%else
Source0: http://download.kde.org/%{stable}/plasma/%{major}/breeze-%{version}.tar.xz
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
BuildRequires: cmake(Plasma) >= 5.90.0
BuildRequires: cmake(Wayland) >= 5.90.0
BuildRequires: cmake(KF6Kirigami2)
BuildRequires: pkgconfig(fftw3)
%if %{with qt5}
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5X11Extras)
BuildRequires: cmake(KF5Kirigami2)
%endif

%description
The KDE 6 Breeze style.

%package qt5
Summary: The Plasma 6 Breeze style for Qt 5.x applications
Group: Graphical desktop/KDE

%description qt5
The Plasma 6 Breeze style for Qt 5.x applications

%package devel
Summary: Devel stuff for %{name}
Group: Development/KDE and Qt
Requires: %{name} = %{EVRD}
Provides: %{name}-devel = %{EVRD}

%description devel
This package contains header files needed if you wish to build applications
based on %{name}.

%prep
%autosetup -p1 -n breeze-%{?git:%{gitbranchd}}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DBUILD_QT5:BOOL=%{?with_qt5:ON}%{!?with_qt5:OFF} \
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
%{_datadir}/icons/breeze_cursors
%{_datadir}/icons/Breeze_Light
%{_datadir}/wallpapers/*
%{_datadir}/kstyle/themes/breeze.themerc
%{_datadir}/QtCurve
%{_datadir}/color-schemes/BreezeDark.colors
%{_datadir}/color-schemes/BreezeLight.colors
%{_qtdir}/plugins/styles/breeze6.so
%{_qtdir}/plugins/org.kde.kdecoration2/*.so
%{_iconsdir}/hicolor/scalable/apps/breeze-settings.svgz
%{_datadir}/color-schemes/BreezeClassic.colors
%{_qtdir}/plugins/kstyle_config/breezestyleconfig.so
%{_datadir}/applications/breezestyleconfig.desktop
%{_datadir}/applications/kcm_breezedecoration.desktop
%dir %{_qtdir}/plugins/org.kde.kdecoration2.kcm
%{_qtdir}/plugins/org.kde.kdecoration2.kcm/kcm_breezedecoration.so

%if %{with qt5}
%files qt5
%{_libdir}/qt5/plugins/styles/breeze5.so
%endif

%files devel
%{_libdir}/cmake/Breeze
