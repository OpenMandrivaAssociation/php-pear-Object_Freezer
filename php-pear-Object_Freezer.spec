%define  upstream_name Object_Freezer

Summary:	Library that faciliates PHP object stores
Name:		php-pear-%{upstream_name}
Version:	1.0.0
Release:	%mkrel 1
License:	BSD
Group:		Development/PHP
URL:		http://www.phpunit.de/
Source0:	http://pear.phpunit.de/get/Object_Freezer-%{version}.tgz
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-cli >= 3:5.2.1
Requires:	php-pear >= 1:1.9.4
Requires:	php-channel-phpunit
BuildArch:	noarch
BuildRequires:	php-pear
BuildRequires:	php-channel-phpunit
Suggests:	php-pear-PHPUnit >= 3.6.3
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PHPUnit is a regression testing framework used by the developer who implements
unit tests in PHP.

This package provides a Library that provides the low-level functionality
required to store ("freeze") PHP objects to and fetch ("thaw") PHP objects
from an object store for PHPUnit.

%prep

%setup -q -c 
mv package.xml %{upstream_name}-%{version}/%{upstream_name}.xml

%build

%install
rm -rf %{buildroot}

cd %{upstream_name}-%{version}
pear install --nodeps --packagingroot %{buildroot} %{upstream_name}.xml
rm -rf %{buildroot}%{_datadir}/pear/.??*

rm -rf %{buildroot}%{_datadir}/pear/docs
rm -rf %{buildroot}%{_datadir}/pear/tests

install -d %{buildroot}%{_datadir}/pear/packages
install -m 644 %{upstream_name}.xml %{buildroot}%{_datadir}/pear/packages

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 201000
pear install --nodeps --soft --force --register-only \
    %{_datadir}/pear/packages/%{upstream_name}.xml >/dev/null || :
%endif

%preun
%if %mdkversion < 201000
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi
%endif

%files
%defattr(-,root,root)
%{_datadir}/pear/Object/Freezer
%{_datadir}/pear/Object/*.php
%{_datadir}/pear/packages/Object_Freezer.xml

