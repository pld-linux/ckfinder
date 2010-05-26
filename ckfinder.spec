Summary:	AJAX file manager for web browsers
Summary(pl.UTF-8):	Edytor tekstowy dla Internetu
Name:		ckfinder
Version:	1.4.2
Release:	0.19
License:	Custom
Group:		Applications/WWW
Source0:	http://download.cksource.com/CKFinder/CKFinder%20for%20PHP/%{version}/%{name}_php_%{version}.tar.gz
# Source0-md5:	0f37b528272f915b9fcd3a12e2f53439
URL:		http://www.ckfinder.com/
Patch0:		error_reporting.patch
Patch1:		paths.patch
Source1:	find-lang.sh
Source2:	apache.conf
Source3:	lighttpd.conf
BuildRequires:	rpmbuild(macros) > 1.268
BuildRequires:	sed >= 4.0
#Requires:	php-gd
Requires:	webapps
Requires:	webserver
Requires:	webserver(access)
Requires:	webserver(alias)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{name}

%define		find_lang	sh %{SOURCE1}

%description
CKFinder is a powerful and easy to use AJAX file manager for web
browsers. Its simple interface makes it intuitive and quick to learn
for all kinds of users, from advanced professionals to Internet
beginners.

%package -n php-%{name}
Summary:	PHP class to create editors instances
Group:		Development/Languages/PHP

%description -n php-%{name}
CKEditor class that can be used to create editor instances in PHP
pages on server side.

%package connector-php
Summary:	File Manager Connector for PHP
Summary(pl.UTF-8):	Interfejs zarządcy plików do PHP
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}
Requires:	php-common >= 4:5.0.0
Requires:	php-gd

%description connector-php
File Manager Connector for PHP.

%description connector-php -l pl.UTF-8
Interfejs zarządcy plików do PHP.

%prep
%setup -qc
# use versioned build dir
mv ckfinder/* .
rmdir ckfinder

# force php5 only
rm core/ckfinder_php4.php
mv core/ckfinder_php5.php ckfinder.php
rm -r core/connector/php/php4
mv core/connector/php/php5/* core/connector/php
rmdir core/connector/php/php5

# undos the files
find '(' -name '*.js' -o -name '*.css' -o -name '*.txt' -o -name '*.html' -o -name '*.php' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

%patch0 -p1
%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},%{php_data_dir},/var/lib/%{name}}

cp -a ckfinder.js $RPM_BUILD_ROOT%{_appdir}
cp -a core/* $RPM_BUILD_ROOT%{_appdir}
cp -a config.php $RPM_BUILD_ROOT%{_sysconfdir}
cp -a ckfinder.php $RPM_BUILD_ROOT%{php_data_dir}

cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a _samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a ckfinder.html $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%find_lang %{name}.lang

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc changelog.txt install.txt license.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php

%dir %{_appdir}
%dir %{_appdir}/connector
%dir %{_appdir}/help
%dir %{_appdir}/skins
%{_appdir}/ckfinder.js
%{_appdir}/css
%{_appdir}/images
%{_appdir}/js
%{_appdir}/pages

%{_appdir}/skins/default
%{_appdir}/skins/office2003
%{_appdir}/skins/silver

%{_appdir}/help/en
%lang(es_MX) %{_appdir}/help/es-mx
%lang(es) %{_appdir}/help/es
%lang(pl) %{_appdir}/help/pl

%dir %attr(770,root,http) /var/lib/%{name}

%{_examplesdir}/%{name}-%{version}

%files connector-php
%defattr(644,root,root,755)
%dir %{_appdir}/connector/php
%{_appdir}/connector/php/connector.php
%{_appdir}/connector/php/constants.php
%{_appdir}/connector/php/CommandHandler
%{_appdir}/connector/php/Core
%{_appdir}/connector/php/ErrorHandler
%{_appdir}/connector/php/Utils

%files -n php-%{name}
%defattr(644,root,root,755)
%{php_data_dir}/ckfinder.php
