%define package_name environment-modules
%define alice_name alice-%{package_name}
%define alice_package_version 1.1.7

Name:		%{alice_name}
Version:	%{alice_package_version}
Release:	1%{?dist}
Summary:	Virtual env package for ALICE
Group:		System Environment/Daemons
License:	LGPLv2+
URL:		http://alicepc104.jinr.ru
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:	aliroot-version

BuildRequires:	environment-modules
Requires:	environment-modules

%description
Virtual env package for ALICE

%prep
cp -p %SOURCE0 .
%build

%install
mkdir -p %{buildroot}/usr/bin
cp %SOURCE0 %{buildroot}/usr/bin/
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/aliroot-version
%changelog
