%define package_name new
%define alice_name aliroot-an-%{package_name}
%define alice_package_version 5.03.70

Name:		%{alice_name}
Version:	%{alice_package_version}
Release:	1%{?dist}
Summary:	Virtual env package for ALICE
Group:		System Environment/Daemons
License:	LGPLv2+
URL:		http://alicepc104.jinr.ru
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	alice-aliroot-an-%{alice_package_version}

%description
Virtual package to have NEW AliRoot

%prep

%build

%install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

%changelog
