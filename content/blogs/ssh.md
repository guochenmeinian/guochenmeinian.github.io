+++
title = "surrounded region"
date = 2025-05-05 
[taxonomies]
tags = ['computer science']
+++


## 🔐 Useful SSH Techniques

Here are some practical SSH techniques I’ve learned and found worth documenting — especially for situations like connecting to remote machines, securely accessing internal web interfaces (e.g. TensorBoard or Jupyter), and managing your own devices (e.g. PC and Mac) across different networks.

Whether you're setting up a home lab, working remotely, or doing machine learning experiments on a server, these techniques can save you a lot of time.

---

### 🧑‍💻 ZeroTier

[ZeroTier](https://www.zerotier.com/) allows you to create a virtual network, making it easy to connect devices like your Mac and PC as if they were on the same LAN.

#### To make your PC the server
##### 1. Install SSH client (to connect to other devices)
```
# Install SSH client (to connect to other devices)
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0

# Install SSH server (to allow incoming connections)
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Verify installation
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'
```

##### 2. Start and Enable the SSH Server
```
# Start the SSH service
Start-Service sshd

# Set SSH service to start automatically
Set-Service -Name sshd -StartupType 'Automatic'
```

##### 3. Find Your Local IP (No need to do this if you're using ZeroTier though)
```
ipconfig
```

#### 🔄 Bonus: Set WSL Default User to Root (Optional)

##### 1. Edit your WSL config file:
```
sudo vi /etc/wsl.conf
```

##### 2. Add the following:
```
[user]
default=root
```

##### 3. Restart WSL to apply the changes.

---

### 🌐 SSH Port Forwarding (Access Remote Web UIs Locally)

After connecting to a remote server via SSH, you can access web interfaces (like TensorBoard running on localhost:6006) from your local machine using SSH port forwarding.

#### Basic Command Format
```
ssh -L local_port:remote_address:remote_port username@remote_ip
```

#### Example: Accessing Remote TensorBoard
```
ssh -L 6006:localhost:6006 username@remote_ip
```
Then open your browser and visit:
```
http://localhost:6006
```

#### Tips
- You can forward multiple ports at once. For example:
    ```
    ssh -L 6006:localhost:6006 -L 8888:localhost:8888 username@remote_ip
    ```
    This maps both TensorBoard (port 6006) and Jupyter Notebook (port 8888) to your local machine.

- This works even if the remote service is bound to 127.0.0.1 on the server, because the forwarding is executed from within the SSH session.

---

### 🖥️ GNU Screen

`screen` lets you create persistent terminal sessions that keep running even if you disconnect (perfect for long-running tasks like training models, servers, etc).

🔧 Common Commands

🎯 Start a new session
```
screen -S mysession
```

🔍 List all screen sessions
```
screen -ls
```

🔁 Reconnect to a session
```
screen -r mysession
```

🔚 Detach (leave it running in background)
Inside screen, press:
```
Ctrl + A, then D
```
🏃 Now your process continues even if you close the terminal.


Hopefully that helps.
