# 关于t #
一个命令行下的Todo任务工具.

思想上来源于sjl写的 [t](https://github.com/sjl/t) ，里面输出短id的函数使用了sjl写的，其余自己重新实现了，加上了日期的输出和排序.

# 安装 #
注意: 因为用到了`argparse`模块, 所以需要 `Python >= 2.7`

把t克隆到本地.

    git clone git@github.com:tankywoo/t.git ~/.t

修改shell配置文件(.bashrc/.zshrc等)
 
    alias t='python ~/.t/t.py --task-dir ~/.tasks --list tasks'

意思就是设置一个alias命令`t`, 任务目录在`~/.tasks`, 任务文件是`tasks`  
这个任务文件夹不需要手动新建, 在查看或新建任务时, 如果没有, 会自动新建.
任务文件名设置为tasks后, 任务目录里会有`tasks`和`.tasks.done`两个文件, 分别表示todo和done两个任务的存储文件.


# 使用方法 #

## 查看TODO任务 ##
直接使用 `t` 命令就可以查看任务
   
    15:27 tankywoo@gentoo-jl /home/tankywoo
    % t
    7 | 06-04 | 测试t工具
    a | 06-04 | 增加t的使用说明

左边是任务的id号, 中间是新增/修改时间, 右边是任务内容

## 查看已完成任务 ##
使用 `t --done` 命令可以查看已完成任务
    
    15:29 tankywoo@gentoo-jl /home/tankywoo
    % t --done
    f | 06-04 | 这是已完成的任务

## 新增任务 ##
使用命令 `t 任务内容` 可以新增任务

    15:29 tankywoo@gentoo-jl /home/tankywoo
    % t 新增任务
    15:30 tankywoo@gentoo-jl /home/tankywoo
    % t
    7  | 06-04 | 测试t工具
    a5 | 06-04 | 新增任务
    af | 06-04 | 增加t的使用说明

## 修改任务 ##
使用 `t -e 任务id 修改后的任务内容`

    15:32 tankywoo@gentoo-jl /home/tankywoo
    % t -e a5 "新增任务(修改后)"
    15:32 tankywoo@gentoo-jl /home/tankywoo
    % t
    7  | 06-04 | 测试t工具
    a5 | 06-04 | 新增任务(修改后)
    af | 06-04 | 增加t的使用说明

## 完成任务 ##
使用 `t -f 任务id` 可以完成指定任务

    15:33 tankywoo@gentoo-jl /home/tankywoo
    % t
    7  | 06-04 | 测试t工具
    a5 | 06-04 | 新增任务(修改后)
    af | 06-04 | 增加t的使用说明
    15:33 tankywoo@gentoo-jl /home/tankywoo
    % t -f a5
    15:33 tankywoo@gentoo-jl /home/tankywoo
    % t
    7 | 06-04 | 测试t工具
    a | 06-04 | 增加t的使用说明
    15:33 tankywoo@gentoo-jl /home/tankywoo
    % t --done
    a | 06-04 | 新增任务(修改后)
    f | 06-04 | 这是已完成的任务

## Undo任务 ##
使用 `t --undo 任务id` 可以把一个已完成的任务重新加入todo列表

## 删除任务 ##
使用 `t -r 任务id` 可以直接删除一个任务

# 一些技巧 #

## 查看todo任务个数 ##

    t | wc -l

## 搜索任务中的关键字 ##

    t | grep 'keyword'

## 多个任务列表 ##
比如可以把任务列表分为 `today` 和 `someday`, 可以在上面提到的shell配置文件中再添加alise命令

    alias today='python ~/.t/t.py --task-dir ~/.tasks --list today'
    alias someday='python ~/.t/t.py --task-dir ~/.tasks --list someday'

这样就可以使用 today 和 someday 命令添加任务到相应任务列表

# 同步问题 #

命令行todo虽然方便, 但是同步却成了一个问题.  

根据我个人的使用, 有以下几个方法(具体过程不详细描述, 可自行Google)

## 使用Dropbox ##
Dropbox 有 `CLI` 版本, 我最开始就用的这个, 不过考虑到间歇性同步失败(你懂的), 所以放弃了.

## rsync ##
如果你有一台 `VPS`, 可以做 rsync 当中间节点, 几台机器都通过 rsync 同步.

## 远程代码托管仓库 ##
比如国外的Github, 国内的Gitcafe等等, 如果不想让别人看见你的任务, 可以弄一个私有仓库.  
当然, 代码托管本来是用于托管代码的, 当作网盘似得放任务不是很厚道 :(

## 还有其他的方法吗? ##
我暂时还没想到其他方法, 如果你有好的方法, 可以给我 email: me@tankywoo.com 或者直接 issue

# 补充 #

## 2013-05-29 ##
如果 `t` 在新增任务时, 任务内容有一些shell内置命令或其他命令, 可能会执行这个命令. 这时需要用单引号`''`或双引号`""`括住任务内容即可.
