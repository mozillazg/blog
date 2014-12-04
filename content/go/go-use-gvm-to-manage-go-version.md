sudo apt-get install curl git mercurial make binutils bison gcc build-essential


bash < <(curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer)

vim gvm-installer

change 

SRC_REPO=${SRC_REPO:-https://github.com/moovweb/gvm.git} 

SRC_REPO=${SRC_REPO:-git://github.com/moovweb/gvm.git} 

bash gvm-installer



 ~$ bash gvm-installer 
Cloning from git://github.com/moovweb/gvm.git to /home/mg/.gvm
Created profile for existing install of Go at "/usr/lib/go"
Installed GVM v1.0.22

Please restart your terminal session or to get started right away run
 `source /home/mg/.gvm/scripts/gvm`
 
  ~$ source /home/mg/.gvm/scripts/gvm
  
   ~$ gvm version
Go Version Manager v1.0.22 installed at /home/mg/.gvm

 ~$ gvm install go1.3
Downloading Go source...
ERROR: Couldn't download Go source. Check the logs /home/mg/.gvm/logs/go-download.log

中止: 失败: Network is unreachable

gvm install go1.3 --source=https://mozillazg@bitbucket.org/mozillazg/go
https://mozillazg@bitbucket.org/mozillazg/go

 imp_api_test$ gvm install go1.3 --source=https://mozillazg@bitbucket.org/mozillazg/go
Downloading Go source...
Installing go1.3...
 * Compiling...
 
  imp_api_test$ gvm list

gvm gos (installed)

   go1.3
   system

 imp_api_test$ 
 
  imp_api_test$ gvm use go1.3
Now using version go1.3
 imp_api_test$ go Version
go: unknown subcommand "Version"
Run 'go help' for usage.
 imp_api_test$ go version
go version go1.3 linux/amd64
 imp_api_test$ 

