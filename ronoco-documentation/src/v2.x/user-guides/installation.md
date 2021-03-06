# Installation
The installation is divide into two parts. First it is necessary to install ROS Noetic and then to install the different modules of ronoco. An installation guide for ROS noetic for Ubuntu is provided below. Refer to [the official page](http://wiki.ros.org/noetic/Installation) for more details

## Ubuntu install of ROS Noetic

Configure your Ubuntu to allow "restricted", "universe" and "multiverse". You can
[follow the Ubuntu guide](https://help.ubuntu.com/community/Repositories/Ubuntu) for instructions on doing this.

Set up your computer to accept software from packages.ros.org

```bash
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" \
> /etc/apt/sources.list.d/ros-latest.list'
```

Set up your keys

```bash
sudo apt install curl # if you haven't already installed curl
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | \ 
sudo apt-key add -
```

First, make sur your Debian package index is up-to-date then install ROS

```bash
sudo apt update
sudo apt install ros-noetic-desktop-full
```

You must source this script in every **bash** terminal you use ROS in

```bash
source /opt/ros/noetic/setup.bash
````

It can be convenient to automatically source this script every time a new shell is launched. These commands will do that
for you
```bash
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source $HOME/.bashrc

#or if you use zsh
echo "source /opt/ros/noetic/setup.zsh" >> ~/.zshrc
source $HOME/.zshrc
```



## Ronoco

To install ronoco you need the following packages:

- npm
- python3
- ROS noetic (also works on ROS melodic)

To start it is necessary to clone the project in the catkin workspace
```bash
#if you haven't got a catkin_ws
mkdir -p $HOME/catkin_ws/src
cd $HOME/catkin_ws/
catkin_make

cd $HOME/catkin_ws/src/
git clone https://github.com/Sdelpeuch/ronoco.git
```

Then you have to install the three modules that constitute ronoco. Firstly *ronoco-nodered* allowing the user to define the behaviour trees of the robot (see How to use it and How to create a behaviour tree). This module depends on Node-RED, so it is necessary to install the framework and then the blocks specific to ronoco.

```bash
sudo npm install -g --unsafe-perm node-red
mkdir $HOME/.node-red/
cd $HOME/.node-red/
npm install $HOME/catkin_ws/src/ronoco/ronoco-nodered/
```

Once *ronoco-nodered* is installed it is necessary to install the web client inside *ronoco-ui*

```bash
cd $HOME/catkin_ws/src/ronoco/ronoco-ui/
npm install
```

Finally, all that remains is to install the application engine found in *ronoco-vm*.

```bash
cd $HOME/catkin_ws/src/ronoco/ronoco-vm/
pip3 install -r requirements.txt
```

Before using ronoco it is necessary to compile the ROS workspace

```bash
cd $HOME/catkin_ws/
catkin_make
source devel/setup.bash

#or if you use zsh
source devel/setup.zsh
```

### Set up Rviz (optionnal)

If you want to view the different points and paths defined by ronoco in rviz it is necessary to add two markers in rviz.

To add a marker in rviz : click on "add" at the bottom left of the screen. A menu opens. Click on "Marker". Then in the menu on the left of your screen (Displays) find "Marker". Scroll down the menu and set the "Marker topic" field to :

1. to view the recorded points: "visualization_marker".
2. (rolling robots only) to view the paths travelled: "path_coverage_marker"

<center>
<img src="../static/marker.gif"></img>
</center>

To start ronoco refer to the [Getting Started](quick-start.md) page