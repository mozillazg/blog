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

git://github.com/jnwhiteh/golang.git
