

git branch -a | grep remotes |grep -v HEAD |grep -v '[\*>]'|sed -e 's/remotes\///g'| xargs -n 1 git push --delete gitlab
git branch -a | grep remotes |sed -e 's/remotes\///g'| xargs -n 100 git push --delete gitlab



git branch -a | grep remotes | grep -v gitlab |sed -e 's/remotes\///g'| xargs -n 100 git push --delete gitlab
git branch -a | grep remotes | grep origin |sed -e 's/remotes\///g'| xargs -n 1 git push --delete gitlab


不过一旦有错误就会终止

| => git push --delete gitlab mine/vendor/stdlib \
| => mine/vendor/stdlib-3.3.5 \
| => mine/vendoring
Warning: Permanently added 'gitlab.com,104.210.2.228' (RSA) to the list of known hosts.
error: unable to delete 'mine/vendor/stdlib': remote ref does not exist
error: failed to push some refs to 'git@gitlab.com:mozillazg/pypy.git'


git branch -a | grep -v gitlab |grep -v '[\*>]' |sed -e 's/remotes\///g'| xargs -n 50 git push --delete gitlab


git branch |grep -v '[\*>]' |sed -e 's/^/upstream\//g' | sed -e 's/ //g'| xargs -n 50 git push --delete gitlab
git push --delete gitlab upstream/master


git branch -a | grep mine |sed -e 's/^\s*remotes\///g'| xargs -n 10 git push --delete gitlab
