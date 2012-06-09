# no debug info is generated
%global debug_package %{nil}

%define package_name aliroot-an
%define alice_name alice-%{package_name}

%define alice_dir /opt/cern/alice
%define alice_prefix %{alice_dir}/%{package_name}/%{version}
%define alice_env_module_dir %{alice_dir}/env_modules

# version and deps
%define alice_package_version 5.03.28
%define openssl_dir %{alice_dir}/openssl/0.9.8x
%define xrootd_dir %{alice_dir}/xrootd/3.0.5
%define alien_dir %{alice_dir}/alien/1.0.14n
%define rootsys_dir %{alice_dir}/root/5.33.02b
%define geant3_dir %{alice_dir}/geant3/1.14.2

Name:		%{alice_name}
Version:	%{alice_package_version}
Release:	1%{?dist}
Summary:	AliRoot for ALICE
Group:		System Environment/Daemons
License:	LGPLv2+ 
URL:		http://aliceinfo.cern.ch/
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	alice-geant3 alice-root alice-root-net-alien alice-xrootd alice-openssl environment-modules cmake
Requires:	alice-geant3 alice-root alice-root-net-alien alice-xrootd alice-openssl environment-modules

# define alice dir sctucture

%description
AliRoot for ALICE

%prep
%setup -q -n %{name}-%{version}

%build
export ROOTSYS="%{rootsys_dir}"
export GEANT3="%{geant3_dir}"
export LD_LIBRARY_PATH="%{geant3_dir}/lib/tgt_$ALICE_TARGET:%{rootsys_dir}/lib:%{alien_dir}/lib:%{xrootd_dir}/lib:%{openssl_dir}/lib:$LD_LIBRARY_PATH"
export PATH="%{rootsys_dir}/bin:$PATH"
export ALICE_TARGET="$(root-config --arch)"
export ALICE_INSTALL="%{alice_prefix}"
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
export PATH="%{rootsys_dir}/bin:$PATH"
export ALICE_TARGET="$(root-config --arch)"
# create module file

mkdir -p %{buildroot}%{alice_prefix}/etc/modulefiles
cat > %{buildroot}%{alice_prefix}/etc/modulefiles/%{alice_name}-%{alice_package_version}-%{_arch} <<EOF
#%Module 1.0
# 
# AliRoot module for use with 'environment-modules' package:
# 
prepend-path            PATH            %{xrootd_dir}/bin
prepend-path            PATH            %{alien_dir}/bin
prepend-path            PATH            %{rootsys_dir}/bin
prepend-path            PATH            %{alice_prefix}/bin/tgt_$ALICE_TARGET
prepend-path            LD_LIBRARY_PATH %{openssl_dir}/lib
prepend-path            LD_LIBRARY_PATH %{xrootd_dir}/lib
prepend-path            LD_LIBRARY_PATH %{alien_dir}/lib
prepend-path            LD_LIBRARY_PATH %{rootsys_dir}/lib
prepend-path            LD_LIBRARY_PATH %{geant3_dir}/lib/tgt_$ALICE_TARGET
prepend-path            LD_LIBRARY_PATH %{alice_prefix}/lib/tgt_$ALICE_TARGET
setenv                  ALICE_ROOT      %{alice_prefix}
setenv                  ALICE           %{alice_dir}
setenv                  ALICE_TARGET    $ALICE_TARGET
setenv                  X509_CERT_DIR   %{alien_dir}/share/certificates
setenv                  GSHELL_NO_GCC   1
setenv                  GSHELL_ROOT     %{alien_dir}
EOF

mkdir -p %{buildroot}/etc/modulefiles
cp %{buildroot}%{alice_prefix}/etc/modulefiles/%{alice_name}-%{alice_package_version}-%{_arch} %{buildroot}/etc/modulefiles/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{alice_prefix}
#%{alice_prefix}/bin
#%{alice_prefix}/lib
#%{alice_prefix}/include
#%{alice_prefix}/etc
#%{alice_prefix}/data
#%{alice_prefix}/ANALYSIS
#%{alice_prefix}/EVE
#%{alice_prefix}/FMD
#%{alice_prefix}/LHAPDF
#%{alice_prefix}/MUON
#%{alice_prefix}/OADB
#%{alice_prefix}/OCDB
#%{alice_prefix}/PHOS
#%{alice_prefix}/PWGCF
#%{alice_prefix}/PWGGA
#%{alice_prefix}/PWGHF
#%{alice_prefix}/PWGLF
#%{alice_prefix}/PWGPP
#%{alice_prefix}/QAref
#%{alice_prefix}/TOF
#%{alice_prefix}/TPC
/etc/modulefiles/%{alice_name}-%{alice_package_version}-%{_arch}

%changelog
