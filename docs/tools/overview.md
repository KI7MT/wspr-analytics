Choosing an operating system is rather like picking out a car these days. One can go from mild to wild and 
everyting in between. My personal preference is Linux, with MacOS a very close second. If I were traveling
for work, I'd be on a Mac, no question about it.

For an application-toolset being used with `Spark`, I do not recommend Windows, and will not be showing
installaiton examples for it. If you must use a Windows Laptop or Workstation, I would highly recommend
installing `Virtualbox` and create a virtual machine for all things `Spark` related. The `Virtualbox`
instructions will cover installtion on Windows as well as `Vagrant`. Aside from that, all actions will
take place in a standard Ubuntu 20.04 LTS desktop environment.

Where paractical, examples will include additional mainstream Linux distributions such as: Alpine, CentOS,
Fedora, Debian, Mint, etc. The vast majority of computational work takes place on the command-line
or in Jupyter notebooks. There is no need for a heavyweight desktop unless you want / need it for other
applications. The choice is entirely up to you, however, the more resources you take up with a heavy
desktop environment, the less you have available for computing power.

## Hardware Considerations

There is no question about it, the more CPU cores and RAM you have, then faster results can be resturned.
Use SSD's, where ever possible, and pack the system with as much memory as you can.

While you can run spark jobs on minimal hardware, it's recommendecd to have at least 4 CPU cores and
2GB of RAM per node. I would consider the the bar minimum for small job.

For those that are ambitious, you can create a three or four node cluster out of Raspbery PI's; one
control node and 3 compute nodes. If you go that reoute, consider the Pi 4 B (4GB / 8GB RAM) options.
Four of those would make a nice little Spark Cluster at a modest cost compared to a High-End
laptop boasting 6 cores (12 threads) and 16 GB RAM.

>NOTE: Remember, Spark Clusters do most of the computing in RAM. It's very fast compared to an HDFS
>approach. If you are going to spend cash, invenst in moderate CPU speeds and large quantities
>of fast ECC RAM. 

## Milti-Distribution Commaons

WHere applicable, Multi-Distribution commands will be show in distribution tabs for eas of reading.

>NOTE: these are just examples, and not intended for execution.

=== "Alpine"
    - Update the package list
    ```bash
    apk update
    ```
    - Add a package
    ```bash
    apk add openssh
    apk add openssh opentp vim
    ```

=== "Ubuntu"
    Upgrade the host System Packages.

    ```shell
    # Run the following command
    sudo apt-get update && sudo apt-get upgrade
    ```

=== "Mint"
    Install a pre-requesite package for VirtualBox.

    ```shell
    # Run the following command
    sudo apt-get update
    sudo apt-get install dkms
    ```

=== "Fedora"
    a. Update your fedora release

    ```bash
    sudo dnf upgrade --refresh
    ```

    b. Install a plugin

    ```bash
    sudo dnf install dnf-plugin-system-upgrade
    ```

    c. Download upgraded packages
    ```bash
    sudo dnf system-upgrade download --refresh --releasever=33
    ```
