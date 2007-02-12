Summary:	Sequoia database clustering solution
Summary(pl.UTF-8):   Sequoia - rozwiązanie klastrowe dla baz danych
Name:		sequoia
Version:	3.0
%define	_rc	beta1
Release:	0.%{_rc}.1
License:	Apache Software License 2.0
Group:		Applications
Source0:	https://forge.continuent.org/frs/download.php/192/%{name}-%{version}-%{_rc}-bin.tar.gz
# Source0-md5:	1ec15de01581707635d80bd4ab8a12c6
URL:		http://sequoia.continuent.org/HomePage
BuildRequires:	rpmbuild(macros) >= 1.280
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(sequoia)
Provides:	user(sequoia)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sequoia database clustering solution.

%description -l pl.UTF-8
Sequoia - rozwiązanie klastrowe dla baz danych.

%package doc
Summary:	Sequoia documentation
Summary(pl.UTF-8):   Dokumentacja dla projektu Sequoia
Group:		Documentation

%description doc
Sequoia documentation.

%description doc -l pl.UTF-8
Dokumentacja dla projektu Sequoia.

%prep
%setup -q -n %{name}-%{version}-%{_rc}-bin

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,sysconfig,sequoia} \
	   $RPM_BUILD_ROOT%{_javadir}/%{name} \
	   $RPM_BUILD_ROOT/var/{log/{archiv,}/%{name},lib/%{name}/backup} \

cp -r config/* $RPM_BUILD_ROOT/etc/%{name}
ln -s /etc/%{name} $RPM_BUILD_ROOT%{_javadir}/%{name}/config

for dir in 3rdparty drivers lib xml; do
	cp -r $dir $RPM_BUILD_ROOT/%{_javadir}/%{name}
done

install -D bin/controller.sh ${RPM_BUILD_ROOT}/%{_sbindir}/sequoia_controller
install bin/console.sh ${RPM_BUILD_ROOT}/%{_sbindir}/sequoia_console

#install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/sequoia

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 189 sequoia
%useradd -u 189 -d %{_javadir}/%{name} -s /bin/false -g sequoia -c "Sequoia Cluster" sequoia

%postun
if [ "$1" = "0" ]; then
	%userremove sequoia
	%groupremove sequoia
fi

%if %{with initscript}
%post init
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun init
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi
%endif

%files
%defattr(644,root,root,755)
%{_sysconfdir}/%{name}
#%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
%{_javadir}/%{name}
%attr(755,root,root) %{_sbindir}/*
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(750,sequoia,sequoia) %dir /var/log/%{name}
%attr(750,sequoia,sequoia) %dir /var/log/archiv/%{name}

%if 0
# if _sysconfdir != /etc:
#%%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%endif

%if %{with initscript}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%endif

%files doc
%defattr(644,root,root,755)
%doc doc/*
