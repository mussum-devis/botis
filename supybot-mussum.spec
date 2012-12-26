Name:         supybot-mussum
Version:      1.0
Release:      0.sles11
License:      BSD License
Vendor:       None
Packager:     Rodrigo Dias Cruz
Group:        Internet
Summary:      Plugins for supybot
Source:       %{name}-%{version}.tar.gz
BuildRoot:    %{_tmppath}/%{name}-%{version}
Requires:     supybot
BuildArch:    noarch

%description
TBD

# Use gzip (level 9) compression to work in all distros
%global _binary_payload w9.gzdio
%global _source_payload w9.gzdio

# Use MD5 for file digest (backwards compatible)
%global _binary_filedigest_algorithm 1
%global _source_filedigest_algorithm 1

%prep
%setup

%install
mkdir -p %{buildroot}/usr/share/supybot-mussum/
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/etc/

cp -a plugins/ %{buildroot}/usr/share/supybot-mussum/
cp -a conf/ %{buildroot}/usr/share/supybot-mussum/
cp -a etc/mussum.conf %{buildroot}/etc/
cp -a supybot-mussum %{buildroot}/usr/bin/


%clean
[ %{buildroot} != "/" ] && rm -rf %{buildroot}

%files
/usr/share/supybot-mussum/
/usr/bin/supybot-mussum
/etc/mussum.conf
