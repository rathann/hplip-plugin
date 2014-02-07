%ifarch i686
%global arch x86_32
%endif
%ifarch x86_64
%global arch x86_64
%endif

# Tweak to have debuginfo - part 1/2
%define __debug_install_post %{_builddir}/%{?buildsubdir}/find-debuginfo.sh %{_builddir}/%{?buildsubdir}\
%{nil}

#%%define __provides_exclude_from ^%{_libdir}/hplip/.*/plugins/.*\.so$

Summary: Binary-only plugins for HP multi-function devices, printers and scanners
Name: hplip-plugins
Version: 3.13.11
Release: 2
URL: http://hplipopensource.com/hplip-web/index.html
# list of URLs: http://hplip.sourceforge.net/plugin.conf
Source0: http://www.openprinting.org/download/printdriver/auxfiles/HP/plugins/hplip-%{version}-plugin.run
# extracted from hplip-%%{version}.tar.gz
# data/rules/hplip-printer@.service
Source2: hplip-printer@.service
# config_usb_printer.py
Source3: config_usb_printer.py
License: Distributable, no modification permitted
ExclusiveArch: i686 x86_64
BuildRequires: systemd
Requires: hplip = %{version}
Requires: hplip-firmware = %{version}-%{release}

%description
Binary-only plugins for the following HP multi-function devices,
printers and scanners:

HP Color LaserJet 1600
HP Color LaserJet 2600n
HP Color LaserJet 3500
HP Color LaserJet 3500n
HP Color LaserJet 3550
HP Color LaserJet 3550n
HP Color LaserJet 3600
HP Color LaserJet CM1015
HP Color LaserJet CM1017
HP Color LaserJet CM1312 MFP
HP Color LaserJet CM1312nfi MFP
HP Color LaserJet CM2320 MFP
HP Color LaserJet CM2320fxi MFP
HP Color LaserJet CM2320n MFP
HP Color LaserJet CM2320nf MFP
HP Color LaserJet CP1215
HP LaserJet 1000
HP LaserJet 1005 Series
HP LaserJet 1018
HP LaserJet 1020
HP LaserJet 1022
HP LaserJet 1022n
HP LaserJet 1022nw
HP LaserJet CP1025
HP LaserJet CP1025nw
HP LaserJet M1005
HP LaserJet M1120 MFP
HP LaserJet M1120n MFP
HP LaserJet M1319f MFP
HP LaserJet M1522 MFP
HP LaserJet M1522n MFP
HP LaserJet M1522nf MFP
HP LaserJet M2727 MFP
HP LaserJet M2727nf MFP
HP LaserJet M2727nfs MFP
HP LaserJet P1005
HP LaserJet P1006
HP LaserJet P1007
HP LaserJet P1008
HP LaserJet P1009
HP LaserJet P1505
HP LaserJet P1505n
HP LaserJet P2014
HP LaserJet P2014n
HP LaserJet P2035
HP LaserJet P2035n
HP LaserJet Professional M1217nfw MFP
HP LaserJet Professional P1102
HP LaserJet Professional P1102W
HP LaserJet Professional P1132
HP LaserJet Professional P1136
HP LaserJet Professional P1212nf
HP LaserJet Professional P1566
HP LaserJet Professional P1606

%package -n hplip-firmware
Summary: Firmware for HP multi-function devices, printers and scanners
BuildArch: noarch

%description -n hplip-firmware
Firmware for the following HP multi-function devices, printers and scanners:

HP LaserJet 1000
HP LaserJet 1005 Series
HP LaserJet 1018
HP LaserJet 1020
HP LaserJet P1005
HP LaserJet P1006
HP LaserJet P1007
HP LaserJet P1008
HP LaserJet P1009
HP LaserJet P1505
HP LaserJet Professional P1102
HP LaserJet Professional P1102W
HP LaserJet Professional P1566

%prep
%setup -T -c %{name}-%{version}
chmod +x %{SOURCE0}
%{SOURCE0} --keep --noexec --target $RPM_BUILD_DIR/%{name}-%{version}

# Tweak to have debuginfo - part 2/2
cp -p %{_prefix}/lib/rpm/find-debuginfo.sh .
sed -i -e 's|strict=true|strict=false|' find-debuginfo.sh

%build
echo nothing to build

%install
mkdir -p %{buildroot}{%{_bindir},%{_udevrulesdir},%{_unitdir},%{_datadir}/hplip/data/firmware,{%{_libdir},%{_datadir}}/hplip/{data,fax,prnt,scan}/plugins}

install -pm644 %{SOURCE2} %{buildroot}%{_unitdir}/
install -pm755 %{SOURCE3} %{buildroot}%{_datadir}/hplip/
ln -s ../share/hplip/config_usb_printer.py %{buildroot}%{_bindir}/hp-config_usb_printer

install -pm644 hp_laserjet_*.fw.gz %{buildroot}%{_datadir}/hplip/data/firmware/

%ifarch i686 x86_64
install -pm644 license.txt %{buildroot}%{_datadir}/hplip/data/plugins/
install -pm644 plugin.spec %{buildroot}%{_datadir}/hplip/

install -pm755 fax_marvell-%{arch}.so %{buildroot}%{_libdir}/hplip/fax/plugins/
ln -s %{_libdir}/hplip/fax/plugins/fax_marvell-%{arch}.so %{buildroot}%{_datadir}/hplip/fax/plugins/fax_marvell.so

install -pm755 lj-%{arch}.so %{buildroot}%{_libdir}/hplip/prnt/plugins/
ln -s %{_libdir}/hplip/prnt/plugins/lj-%{arch}.so %{buildroot}%{_datadir}/hplip/prnt/plugins/lj.so

for drv in marvell soap soapht ; do
  install -pm755 bb_$drv-%{arch}.so %{buildroot}%{_libdir}/hplip/scan/plugins/
  ln -s %{_libdir}/hplip/scan/plugins/bb_$drv-%{arch}.so %{buildroot}%{_datadir}/hplip/scan/plugins/bb_$drv.so
done

mkdir -p %{buildroot}%{_sharedstatedir}/hp
cat >> %{buildroot}%{_sharedstatedir}/hp/hplip.state << __EOF__
[plugin]
installed = 1
eula = 1
version = %{version}

__EOF__
%endif

%files
%doc license.txt
%{_libdir}/hplip
%{_datadir}/hplip/plugin.spec
%{_datadir}/hplip/data/plugins
%{_datadir}/hplip/fax/plugins
%{_datadir}/hplip/prnt/plugins/lj*.so
%{_datadir}/hplip/scan/plugins
%{_sharedstatedir}/hp/hplip.state

%files -n hplip-firmware
%{_bindir}/hp-config_usb_printer
%{_unitdir}/hplip-printer@.service
%{_datadir}/hplip/config_usb_printer.py*
%{_datadir}/hplip/data/firmware

%changelog
* Fri Feb 07 2014 Dominik Mierzejewski <rpm@greysector.net> 3.13.11-2
- drop wrong udev rules file
- move config_usb_printer.py into correct location and add symlink

* Sun Dec 08 2013 Dominik Mierzejewski <rpm@greysector.net> 3.13.11-1
- update to 3.13.11
- reversed Requires
- dropped obsolete specfile constructs

* Wed Oct 02 2013 Dominik Mierzejewski <rpm@greysector.net> 3.13.9-1
- update to 3.13.9
- add missing systemd BR

* Tue Aug 06 2013 Dominik Mierzejewski <rpm@greysector.net> 3.13.7-1
- update to 3.13.7
- synced config_usb_printer.py

* Sat Jun 29 2013 Dominik Mierzejewski <rpm@greysector.net> 3.13.6-1
- update to 3.13.6
- update sysfs rules file from hplip tarball
- install systemd service unit (not included in hplip rpm)
- install hp-config_usb_printer (not included in hplip rpm)

* Sun May 26 2013 Dominik Mierzejewski <rpm@greysector.net> 3.13.5-1
- update to 3.13.5
- updated printer/MFD lists in the descriptions
- install udev rules file from main hplip tarball

* Tue May 21 2013 Dominik Mierzejewski <rpm@greysector.net> 3.13.4-1
- update to 3.13.4

* Sat Apr 20 2013 Dominik Mierzejewski <rpm@greysector.net> 3.13.3-1
- update to 3.13.3
- install hplip.state and plugin.spec
- install license.txt under %%{_datadir}, not %%{_libdir}

* Sun Apr 07 2013 Dominik Mierzejewski <rpm@greysector.net> 3.13.2-1
- update to 3.13.2

* Sun Feb 17 2013 Dominik Mierzejewski <rpm@greysector.net> 3.12.11-1
- update to 3.12.11
- move udev rules to /usr/lib/udev/rules.d, as specified by _udevrulesdir macro
- enable debuginfo
- use ExclusiveArch instead of ExcludeArch
- use strict hplip version Requires

* Sun Jan 06 2013 Dominik Mierzejewski <rpm@greysector.net> 3.12.2-1
- update to 3.12.2
- drop udev rules patch
- replace define with global in macro definitions
- filter the plugins from both Requires and Provides as they're detected incorrectly

* Wed Apr 04 2012 Dominik Mierzejewski <rpm@greysector.net> 3.10.9-1
- initial build
