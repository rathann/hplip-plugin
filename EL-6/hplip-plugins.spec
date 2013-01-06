%global _enable_debug_packages %{nil}
%global debug_package          %{nil}

%ifarch i686
%global arch x86_32
%endif
%ifarch x86_64
%global arch x86_64
%endif

Summary: Binary-only plugins for HP multi-function devices, printers and scanners
Name: hplip-plugins
Version: 3.12.2
Release: 1
URL: http://hplipopensource.com/hplip-web/index.html
Group: System Environment/Libraries
# list of URLs: http://hplip.sourceforge.net/plugin.conf
Source0: http://www.openprinting.org/download/printdriver/auxfiles/HP/plugins/hplip-%{version}-plugin.run
License: Distributable, no modification permitted
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch: arm ppc ppc64 sparc sparc64
Requires: hplip >= %{version}

%description
Binary-only plugins for the following HP multi-function devices,
printers and scanners:

HP Color LaserJet CM1015
HP Color LaserJet CM1017
HP Color LaserJet CM1312 MFP
HP Color LaserJet CM1312nfi MFP
HP Color LaserJet CM2320 MFP
HP Color LaserJet CM2320fxi MFP
HP Color LaserJet CM2320n MFP
HP Color LaserJet CM2320nf MFP
HP LaserJet 1000
HP LaserJet 1005 Series
HP LaserJet 1018
HP LaserJet 1020
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
HP LaserJet P1505
HP LaserJet Professional M1132
HP LaserJet Professional M1136
HP LaserJet Professional M1212nf
HP LaserJet Professional M1217nfw MFP
HP LaserJet Professional P1102
HP LaserJet Professional P1102W
HP LaserJet Professional P1566

%package -n hplip-firmware
Summary: Firmware for HP multi-function devices, printers and scanners
BuildArch: noarch
Requires: hplip-plugins = %{version}-%{release}

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
HP LaserJet P1505
HP LaserJet Professional P1102
HP LaserJet Professional P1102W
HP LaserJet Professional P1566

%prep
%setup -T -c %{name}-%{version}
chmod +x %{SOURCE0}
%{SOURCE0} --keep --noexec --target $RPM_BUILD_DIR/%{name}-%{version}

%build
echo nothing to build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}{/etc/udev/rules.d,%{_datadir}/hplip/data/firmware,{%{_libdir},%{_datadir}}/hplip/{data,fax,prnt,scan}/plugins}

install -pm644 86-hpmud-hp_laserjet_*.rules %{buildroot}/etc/udev/rules.d/

install -pm644 hp_laserjet_*.fw.gz %{buildroot}%{_datadir}/hplip/data/firmware/

%ifarch i686 x86_64
install -pm644 license.txt %{buildroot}%{_libdir}/hplip/data/plugins/

install -pm755 fax_marvell-%{arch}.so %{buildroot}%{_libdir}/hplip/fax/plugins/
ln -s %{_libdir}/hplip/fax/plugins/fax_marvell-%{arch}.so %{buildroot}%{_datadir}/hplip/fax/plugins/fax_marvell.so

install -pm755 lj-%{arch}.so %{buildroot}%{_libdir}/hplip/prnt/plugins/
ln -s %{_libdir}/hplip/prnt/plugins/lj-%{arch}.so %{buildroot}%{_datadir}/hplip/prnt/plugins/lj.so

for drv in marvell soap soapht ; do
  install -pm755 bb_$drv-%{arch}.so %{buildroot}%{_libdir}/hplip/scan/plugins/
  ln -s %{_libdir}/hplip/scan/plugins/bb_$drv-%{arch}.so %{buildroot}%{_datadir}/hplip/scan/plugins/bb_$drv.so
done
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc license.txt
%{_libdir}/hplip
%{_datadir}/hplip/data/plugins
%{_datadir}/hplip/fax/plugins
%{_datadir}/hplip/prnt/plugins/lj*.so
%{_datadir}/hplip/scan/plugins

%files -n hplip-firmware
%defattr(-,root,root,-)
%{_sysconfdir}/udev/rules.d/86-hpmud-hp_laserjet_*.rules
%{_datadir}/hplip/data/firmware

%changelog
* Sun Jan 06 2013 Dominik Mierzejewski <rpm@greysector.net> 3.12.2-1
- update to 3.12.2
- drop udev rules patch
- replace define with global in macro definitions

* Wed Apr 04 2012 Dominik Mierzejewski <rpm@greysector.net> 3.10.9-1
- initial build for EL-6 based on Fedora package
