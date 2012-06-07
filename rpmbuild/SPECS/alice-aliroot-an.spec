# no debug info is generated
%global debug_package %{nil}

Name:		alice-aliroot-an
Version:	5.03.28
Release:	1%{?dist}
Summary:	AliRoot for ALICE
Group:		System Environment/Daemons
License:	LGPLv2+ 
URL:		http://aliceinfo.cern.ch/
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	alice-geant3 cmake
Requires:	alice-geant3

# define alice dir sctucture
%define alice_dir /opt/cern/alice
%define rootsys_dir %{alice_dir}/alice-root/5.33.02b
%define geant3_dir %{alice_dir}/alice-geant3/1.14.2
%define openssl_dir %{alice_dir}/alice-openssl/0.9.8x
%define xrootd_dir %{alice_dir}/alice-xrootd/3.0.5
%define alien_dir %{alice_dir}/alice-alien/1.0.14n 
%define _prefix %{alice_dir}/%{name}/%{version}

%description
AliRoot for ALICE

%prep
%setup -q -n %{name}-%{version}

%build
export ROOTSYS="%{rootsys_dir}"
export GEANT3="%{geant3_dir}"
export ALICE_TARGET="$(root-config --arch)"
export LD_LIBRARY_PATH="%{geant3_dir}/lib/tgt_$ALICE_TARGET:%{rootsys_dir}/lib:%{alien_dir}/lib:%{xrootd_dir}/lib:%{openssl_dir}/lib:$LD_LIBRARY_PATH"
export PATH="%{rootsys_dir}/bin:$PATH"
export ALICE_INSTALL="%{_prefix}"
export ALICE_ROOT="${PWD}"
export ALICE="$(dirname ${ALICE_ROOT})"
mkdir build
cd build
cmake $ALICE_ROOT
make %{?_smp_mflags}
cd %{_builddir}

%install
rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/bin
%{_prefix}/lib
%{_prefix}/include
#%{_prefix}/macros
%{_prefix}/data
%{_prefix}/ANALYSIS
%{_prefix}/EVE
%{_prefix}/FMD
%{_prefix}/LHAPDF
%{_prefix}/MUON
%{_prefix}/OADB
%{_prefix}/OCDB
%{_prefix}/PHOS
%{_prefix}/PWGCF
%{_prefix}/PWGGA
%{_prefix}/PWGHF
%{_prefix}/PWGLF
%{_prefix}/PWGPP
%{_prefix}/QAref
%{_prefix}/TOF
%{_prefix}/TPC

%changelog
