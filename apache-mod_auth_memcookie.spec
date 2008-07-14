#Module-Specific definitions
%define mod_name mod_auth_memcookie
%define mod_conf A53_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache Cookie Authentification Module
Name:		apache-%{mod_name}
Version:	1.0.2
Release:	%mkrel 3
Group:		System/Servers
License:	Apache License
URL:		http://authmemcookie.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/authmemcookie/mod_authmemcookie_v%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
BuildRequires:	libmemcache-devel
BuildRequires:	libevent-devel
Requires:	memcached
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
"Auth MemCookie" are an Apache v2 authentification and authorization modules
are based on "cookie" authentification mecanism. The module don't make
authentification by it self, but verify if authentification "the cookie" are
valid for each url protected by the module. The module validate also if the
"authentificated user" have authorisation to acces url. Authentification are
made externaly by an authentification form page and all authentification
information nessary to the module a stored in memcached indentified by the
cookie value "authentification session id" by this login page.

%prep

%setup -q -n mod_authmemcookie_v%{version}

cp %{SOURCE1} %{mod_conf}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%{_sbindir}/apxs -c mod_auth_memcookie.c -lmemcache

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc docs/* samples/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
