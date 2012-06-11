# no debug info is generated
%global debug_package %{nil}

# version
%define alice_package_version 1.0.14n
# deps versions
%define xrootd_ver 3.0.5

%define package_name alien
%define alice_name alice-%{package_name}

%define alice_dir /opt/cern/alice
%define alice_prefix %{alice_dir}/%{package_name}/%{version}
%define alice_env_module_dir %{alice_dir}/env_modules

# deps
%define xrootd_dir %{alice_dir}/xrootd/%{xrootd_ver}


Name:		%{alice_name}
Version:	%{alice_package_version}
Release:	1%{?dist}
Summary:	AliEn for ALICE
Group:		System Environment/Daemons
License:	BSD
URL:		http://alien.cern.ch/
Source0:	"http://alitorrent.cern.ch/src/xalienfs/xrootd-xalienfs-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	alice-xrootd%{?_isa} = %{xrootd_ver} autoconf libtool chrpath
Requires:	alice-environment-modules
#Requires:	alice-xrootd%{?_isa} = %{xrootd_ver}

%description
AliEn for ALICE

%prep
%setup -q -n xrootd-xalienfs-%{version}

%build
rm -Rf autom4te.cache
./bootstrap.sh
./configure --prefix=%{alice_prefix} \
    --with-certificate-directory=%{alice_prefix}/share \
    --with-xrootd-location=%{xrootd_dir}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
chrpath --delete %{buildroot}%{alice_prefix}/bin/gcp
chrpath --delete %{buildroot}%{alice_prefix}/bin/gprepare
chrpath --delete %{buildroot}%{alice_prefix}/bin/gbbox
chrpath --delete %{buildroot}%{alice_prefix}/bin/gsubmit
chrpath --delete %{buildroot}%{alice_prefix}/bin/gps
chrpath --delete %{buildroot}%{alice_prefix}/bin/gisonline
chrpath --delete %{buildroot}%{alice_prefix}/bin/gshell
chrpath --delete %{buildroot}%{alice_prefix}/bin/gstage

# creating module file
mkdir -p %{buildroot}%{alice_prefix}/etc/modulefiles
cat > %{buildroot}%{alice_prefix}/etc/modulefiles/%{alice_name}-%{alice_package_version}-%{_arch} <<EOF
#%Module 1.0
#
# AliRoot module for use with 'environment-modules' package:
#
prepend-path            PATH            %{xrootd_dir}/bin
prepend-path            PATH            %{alien_dir}/bin
prepend-path            LD_LIBRARY_PATH %{openssl_dir}/lib
prepend-path            LD_LIBRARY_PATH %{xrootd_dir}/lib
prepend-path            LD_LIBRARY_PATH %{alien_dir}/lib
setenv                  OPENSSL_DIR     %{openssl_dir}
setenv                  XROOTD_DIR      %{xrootd_dir}
setenv                  ALIEN_DIR       %{alien_dir}
setenv                  X509_CERT_DIR   %{alien_dir}/share/certificates
setenv                  GSHELL_NO_GCC   1
setenv                  GSHELL_ROOT     %{alien_dir}
EOF


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{alice_prefix}/bin
%{alice_prefix}/lib
%{alice_prefix}/include
%{alice_prefix}/share
%{alice_prefix}/etc

%changelog
