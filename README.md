# turtle_square

## 项目简介

本项目基于 ROS Noetic 和 turtlesim，实现小海龟正方形轨迹绘制。程序通过编写 Python 节点 `draw_square.py`，控制小海龟在 turtlesim 窗口中完成正方形运动轨迹。

## 节点结构

功能包名称：

```text
turtle_square
```

主要文件结构：

```text
turtle_square/
├── CMakeLists.txt
├── package.xml
├── README.md
└── scripts/
    └── draw_square.py
```

节点名称：

```text
draw_square_node
```

主要代码文件：

```text
scripts/draw_square.py
```

主要话题与服务：

```text
发布话题：/turtle1/cmd_vel
订阅话题：/turtle1/pose
使用服务：/clear
使用服务：/turtle1/set_pen
使用服务：/turtle1/teleport_absolute
```

其中，`/turtle1/cmd_vel` 用于控制小海龟运动，`/turtle1/pose` 用于获取小海龟当前位置和朝向，相关服务用于清空画布、设置画笔和移动小海龟起点。

## 启动方式

### 1. 编译工作空间

```bash
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

### 2. 启动 roscore

打开第一个终端：

```bash
roscore
```

### 3. 启动 turtlesim

打开第二个终端：

```bash
rosrun turtlesim turtlesim_node
```

### 4. 运行正方形轨迹节点

打开第三个终端：

```bash
source ~/catkin_ws/devel/setup.bash
rosrun turtle_square draw_square.py
```

运行后，小海龟会在 turtlesim 窗口中自动绘制正方形轨迹。

