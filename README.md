# GitBook-auto-summary
Automatically update `SUMMARY.md` of a GitBook repo，default Based on the markdown title, not the article name，But if without a title, article name is used instead.


##  1. 背景

我们了解 gitbook plugin summary 自动生成 summary.md 文件内容
这是`book sm`命令依赖markdown文章名字组成目录结构的样子。

```bash
$ npm install gitbook-plugin-summary
$ npm install -g gitbook-summary
$ book sm
Finished, generated 'SUMMARY.md' successfully.
$ cat SUMMARY.md 
# Git Handbook

- Git
  * [2 Git Practice](Git/2_git_practice.md)
- Gitbook
  * [1 Gitbook Start](Gitbook/1_gitbook_start.md)
  * [2 Gitbook Plugin Summary](Gitbook/2_gitbook-plugin-summary.md)
  * [3 Github Pages Gitbook](Gitbook/3_github_pages_gitbook.md)
- Github
  * [1 Github Introduce](Github/1_github_introduce.md)
  * [2 Github Local Pull Github](Github/2_github_local_pull_github.md)
  * [3 Github Action](Github/3_github_action.md)
  * [4 Github Page](Github/4_github_page.md)
- Gitlab
  * [1 Gitlab Start](Gitlab/1_gitlab_start.md)
  * [2 Gitlab Deploy](Gitlab/2_gitlab_deploy.md)
  * [3 Gitlab Config](Gitlab/3_gitlab_config.md)
  * [4 Gitlab Runner Deploy](Gitlab/4_gitlab_runner_deploy.md)
  * [5 Gitlab Runner Management](Gitlab/5_gitlab_runner_management.md)
```
但我的需求是可以依据文章标题来生成整个结构，因为如果你有一批大量的markdown文章一个一个手写改动、添加、删除都是一件非常麻烦的事。

我发现来自[mofhu/GitBook-auto-summary](https://github.com/mofhu/GitBook-auto-summary)的功能接近我的需求。

```bash
 $ python3 gitbook-auto-summary.py -h
usage: gitbook-auto-summary.py [-h] [-o] [-a] directory

positional arguments:
  directory        the directory of your GitBook root

optional arguments:
  -h, --help       show this help message and exit
  -o, --overwrite  overwrite on SUMMARY.md
  -a, --append     append on SUMMARY.md
```
功能：
1. 可以通过`-o`覆盖已有的`SUMMARY.md`
2. 新生成一个`SUMMARY-GitBook-auto-summary.md`
3. 还可以通过-a实现追加内容。

##  2. 需求

但这离我渴望的需求还差一点点，那就是当文章内容存在标题，我更选择它来做链接名片，当不存在标题再去依赖文章名字（英文或中文）作为链接名片。并且在`gitbook-auto-summary.py`脚本当前目录我还可以让一些无关的目录作为例外。比如：`node_modules`

我把它实现了。

## 3. 代码
代码：[@ghostwritten/GitBook-auto-summary](https://github.com/Ghostwritten/GitBook-auto-summary)

我们验证它的效果。

##  4. demo

### 4.1  `SUMMARY.md` 添加文章
添加`README.md`
```bash
$ ls
gitbook-auto-summary.py  README.md
root@yourdomain:~/example/summary-demo# python3 gitbook-auto-summary.py .
GitBook auto summary: . 
- [序言](./README.md)

GitBook auto summary finished:) 
root@yourdomain:~/example/summary-demo# ls
gitbook-auto-summary.py  README.md  SUMMARY.md
root@yourdomain:~/example/summary-demo# cat SUMMARY.md 
# Summary

- [序言](./README.md)
```
###  4.2 `SUMMARY.md` 添加目录
创建`Git`目录，并新增格式`.md`与`.markdown`格式文章。
```bash
$ ls Git/
1_git_introduce.markdown  2_git_practice.md
//查看是否有标题
$ head -n 1 Git/1_git_introduce.markdown 
# git 介绍 
$ head -n 1 Git/2_git_practice.md 
# git 实践

$ python3 gitbook-auto-summary.py .
GitBook auto summary: . 
- [序言](./README.md)

- Git

  - [git 介绍](Git/1_git_introduce.markdown)

  - [git 实践](Git/2_git_practice.md)

GitBook auto summary finished:) 
root@yourdomain:~/example/summary-demo# ls
Git  gitbook-auto-summary.py  README.md  SUMMARY-GitBook-auto-summary.md  SUMMARY.md
```
注意默认情况下（`python3 gitbook-auto-summary.py .`）当已存在 `SUMMARY.md`，脚本不会破坏已有`SUMMARY.md`。而是会生成新的文件：`SUMMARY-GitBook-auto-summary.md` 

```bash
$ cat SUMMARY-GitBook-auto-summary.md 
# Summary

- [序言](./README.md)
- Git
  - [git 介绍](Git/1_git_introduce.markdown)
  - [git 实践](Git/2_git_practice.md)

$ cat SUMMARY.md 
# Summary

- [序言](./README.md)
```

###  4.3 `SUMMARY.md` 添加子目录
添加子目录并且添加一篇markdown文章。
```bash
ls Git/
1_git_introduce.markdown  2_git_practice.md  3_git_remote_repo.md  git_command
root@yourdomain:~/example/summary-demo# ls Git/git_command/
2_git_command.md
root@yourdomain:~/example/summary-demo# head -n 1 Git/git_command/2_git_command.md 
# git 命令
```
执行如下：

```bash
$ python3 gitbook-auto-summary.py -o .
$ cat SUMMARY.md 
# Summary

- [序言](./README.md)
- Git
  - [git 介绍](Git/1_git_introduce.markdown)
  - git_command
    - [git 命令](Git/git_command/2_git_command.md)
  - [git 实践](Git/2_git_practice.md)
```

### 4.4 `SUMMARY.md` 覆盖
如果你只想覆盖`SUMMARY.md` 而已。可以`python3 gitbook-auto-summary.py -o .`实现。

```bash
$ python3 gitbook-auto-summary.py -o  .
GitBook auto summary: . --overwrite 
- [序言](./README.md)

- Git

  - [git 介绍](Git/1_git_introduce.markdown)

  - [git 实践](Git/2_git_practice.md)

GitBook auto summary finished:) 
root@yourdomain:~/example/summary-demo# cat SUMMARY.md 
# Summary

- [序言](./README.md)
- Git
  - [git 介绍](Git/1_git_introduce.markdown)
  - [git 实践](Git/2_git_practice.md)
```

有些情况，你可能认为覆盖比较危险，但又不想备份它，只想在原有的基础上追加内容。我们可以`python3 gitbook-auto-summary.py -a .`实现。

###  4.5 `SUMMARY.md` 追加

在Git目录新添了一篇文章。
```bash
$ ls Git/
1_git_introduce.markdown  2_git_practice.md  3_git_remote_repo.md
```
并且我手动改一下 `SUMMARY.md` 内容做一个标记。把`git 介绍`改成`git xxx`

```bash
# Gitbook-Handbook

- [序言](./README.md)
- Git
  - [git xxx](Git/1_git_introduce.markdown)
  - [git 实践](Git/2_git_practice.md)

ls
Git  gitbook-auto-summary.py  README.md  SUMMARY.md
```
执行`python3 gitbook-auto-summary.py -a  .`，`SUMMARY.md`修改的`xxx`并没有被覆盖掉。
```bash
$ python3 gitbook-auto-summary.py -a  .
$ cat SUMMARY-GitBook-auto-summary.md 
# Summary

- [序言](./README.md)
- Git
  - [git xxx](Git/1_git_introduce.markdown)
  - [github 管理远程仓库](Git/3_git_remote_repo.md)
  - [git 实践](Git/2_git_practice.md)
```
如果直接在`SUMMARY.md`追加。执行如下：

```bash
$ python3 gitbook-auto-summary.py -a -o  .
$ cat SUMMARY.md 
# Summary

- [序言](./README.md)
- Git
  - [git xxx](Git/1_git_introduce.markdown)
  - [github 管理远程仓库](Git/3_git_remote_repo.md)
  - [git 实践](Git/2_git_practice.md)
```

当去掉`-a`参数，覆盖重新生成。

```bash
$ python3 gitbook-auto-summary.py  -o  .
$ cat SUMMARY.md 
# Summary

- [序言](./README.md)
- Git
  - [git 介绍](Git/1_git_introduce.markdown)
  - [github 管理远程仓库](Git/3_git_remote_repo.md)
  - [git 实践](Git/2_git_practice.md)
```

### 4.6  `SUMMARY.md`忽略
我们创建一个目录`img`，也许你会用来存储图片。

```bash
$ mkdir img

$ ls
Git  gitbook-auto-summary.py  img  README.md  SUMMARY.md
```
修改代码第十行列表添加`'img'`

```bash
 ignore_list = ['_book', 'node_modules', 'img']
```
执行如下：

```bash
$ python3 gitbook-auto-summary.py  -o  .
$ cat SUMMARY.md 
# Summary

- [序言](./README.md)
- Git
  - [git 介绍](Git/1_git_introduce.markdown)
  - [github 管理远程仓库](Git/3_git_remote_repo.md)
  - [git 实践](Git/2_git_practice.md)
```
大纲并没有收到影响。因为`img`目录已被当作例外。

### 4.7 `SUMMARY.md`替代
当markdown没有标题的时候，也就是说第一行内容为空，我们判断认定为标题不存在。`“#  xxxx”`在其他行并不会被发现。这个时候我们会默认以文章名字作为链接名片。

我们把`Git/git_commnad/2_git_command.md`文章第一行的标题去掉或者下移一行。

```bash
$ head -n 2 Git/git_command/2_git_command.md 
<空行>
# git 命令
```
执行如下：

```bash
$ python3 gitbook-auto-summary.py -o .
$ cat SUMMARY.md 
# Summary

- [序言](./README.md)
- Git
  - [git 介绍](Git/1_git_introduce.markdown)
  - git_command
    - [2_git_command](Git/git_command/2_git_command.md)
  - [github 管理远程仓库](Git/3_git_remote_repo.md)
  - [git 实践](Git/2_git_practice.md)
```
这也是最初`book sm`命令结果的样子。

### 4.8  文章排序
这是超过10数量的文章。
```bash
$  ls Docker-Swarm/
docker_swarm_10_maintenance_mode.md  docker_swarm_6_healthcheck.md
docker_swarm_1_start.md              docker_swarm_7_update.md
docker_swarm_2_network.md            docker_swarm_8_UI_Portainer.md
docker_swarm_3_load_balancing.md     docker_swarm_9_docker-compose_deploy_app.md
docker_swarm_4_encrypted_network.md  README.md
docker_swarm_5_secrets.md            SUMMARY.md
```

book sm执行的效果是这样，`docker_swarm_10_maintenance_mode.md`并没有按照正常的顺序排在`docker_swarm_9_docker-compose_deploy_app.md`的后面。

```bash
- [Docker Swarm](Docker-Swarm/README.md)
  * [Docker Swarm 1 Start](Docker-Swarm/docker_swarm_1_start.md)
  * [Docker Swarm 10 Maintenance Mode](Docker-Swarm/docker_swarm_10_maintenance_mode.md)
  * [Docker Swarm 2 Network](Docker-Swarm/docker_swarm_2_network.md)
  * [Docker Swarm 3 Load Balancing](Docker-Swarm/docker_swarm_3_load_balancing.md)
  * [Docker Swarm 4 Encrypted Network](Docker-Swarm/docker_swarm_4_encrypted_network.md)
  * [Docker Swarm 5 Secrets](Docker-Swarm/docker_swarm_5_secrets.md)
  * [Docker Swarm 6 Healthcheck](Docker-Swarm/docker_swarm_6_healthcheck.md)
  * [Docker Swarm 7 Update](Docker-Swarm/docker_swarm_7_update.md)
  * [Docker Swarm 8 UI Portainer](Docker-Swarm/docker_swarm_8_UI_Portainer.md)
  * [Docker Swarm 9 Docker Compose Deploy App](Docker-Swarm/docker_swarm_9_docker-compose_deploy_app.md)
```
那看我的。`docker_swarm_10_maintenance_mode.md`按照正常的顺序排在`docker_swarm_9_docker-compose_deploy_app.md`的后面。

```bash
$ python3 gitbook-auto-summary.py .
$ cat SUMMARY-GitBook-auto-summary.md
# Summary

* [summary](./Overview.md)
* [序言](./README.md)
- Docker-Swarm
  * [docker swarm 介绍](Docker-Swarm/README.md)
  * [docker swarm 快速入门](Docker-Swarm/docker_swarm_1_start.md)
  * [docker swarm 网络](Docker-Swarm/docker_swarm_2_network.md)
  * [docker swam 集群实现负载均衡](Docker-Swarm/docker_swarm_3_load_balancing.md)
  * [docker swarm 创建加密覆盖网络](Docker-Swarm/docker_swarm_4_encrypted_network.md)
  * [docker swarm 管理 secrets](Docker-Swarm/docker_swarm_5_secrets.md)
  * [docker swarm 健康检查](Docker-Swarm/docker_swarm_6_healthcheck.md)
  * [dcoker swarm 更新](Docker-Swarm/docker_swarm_7_update.md)
  * [docker swarm 部署界面 ui portainer](Docker-Swarm/docker_swarm_8_UI_Portainer.md)
  * [docker swarm 通过 docker compose 部署应用](Docker-Swarm/docker_swarm_9_docker-compose_deploy_app.md)
  * [docker swarm 维护模式](Docker-Swarm/docker_swarm_10_maintenance_mode.md)
```



参考：

 - [mofhu/GitBook-auto-summary](http://frank-the-obscure.me/GitBook-auto-summary/)


![在这里插入图片描述](https://img-blog.csdnimg.cn/5caf2d895e41482ab69e909f8a0c8353.gif#pic_center)
