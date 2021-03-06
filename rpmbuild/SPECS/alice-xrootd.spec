# no debug info is generated
%global debug_package %{nil}
# define alice dir sctucture

# version
%define alice_package_version 3.0.5
# deps versions
%define openssl_ver 0.9.8x

%define alice_dir /opt/cern/alice
%define package_name xrootd
%define alice_name alice-%{package_name}
%define alice_prefix %{alice_dir}/%{package_name}/%{version}
%define alice_prefix %{alice_dir}/%{package_name}/%{alice_package_version}
%define alice_env_module_dir %{alice_dir}/env_modules

# version and deps
%define openssl_dir %{alice_dir}/openssl/%{openssl_ver}

Name:		%{alice_name}-%{alice_package_version}
Version:	0
Release:	0%{?dist}
Summary:	Xroots for ALICE
Group:		System Environment/Daemons
License:	BSD
URL:		http://www.xrootd.org/
Source0:	http://xrootd.slac.stanford.edu/download/v%{alice_package_version}/xrootd-%{alice_package_version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	alice-openssl-%{openssl_ver}
Requires:	alice-environment-modules
#Requires:	alice-openssl%{?_isa} = %{openssl_ver}

%description
Xrootd for ALICE

%prep
%setup -q -n xrootd-%{alice_package_version}

%build
export LD_LIBRARY_PATH="%{openssl_dir}/lib:$LD_LIBRARY_PATH"
./configure.classic --prefix=%{buildroot}%{alice_prefix} --with-ssl-incdir=%{openssl_dir}/include --with-ssl-libdir=%{openssl_dir}/lib \
  --enable-gsi --enable-secssl --no-arch-subdirs --disable-posix --disable-bonjour
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}%{alice_prefix}
rm -Rf %{buildroot}%{alice_prefix}/etc

# creating module file
mkdir -p %{buildroot}%{alice_prefix}/etc/modulefiles
cat > %{buildroot}%{alice_prefix}/etc/modulefiles/%{alice_name}-%{alice_package_version}-%{_arch} <<EOF
#%Module 1.0
#
# AliRoot module for use with 'environment-modules' package:
#
prepend-path            PATH            %{alice_prefix}/bin
prepend-path            LD_LIBRARY_PATH %{openssl_dir}/lib
prepend-path            LD_LIBRARY_PATH %{alice_prefix}/lib
setenv                  OPENSSL_DIR     %{openssl_dir}
setenv                  XROOTD_DIR      %{alice_prefix}
EOF


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{alice_prefix}

%changelog
