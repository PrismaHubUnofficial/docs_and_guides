# Lab Workstation – Overview and General Usage

The Prisma Lab workstation is a shared high-performance compute machine dedicated to physics simulation, robot learning, model training, and heavy computational tasks.

---

## Architecture & Container-First Principle

!!! tip "Always Prefer Docker"
    Whatever workload or experiment you need to run on the workstation, **always run it inside a Docker container**.  
    Running containerized environments keeps the host operating system clean, avoids package version conflicts across users, and guarantees reproducible experimental setups.

### Shared Docker Images Registry

!!! warning "Check Before Creating or Pulling New Images (Disk Conservation)"
    Docker images for robotics, deep learning, and physics simulation (CUDA, PyTorch, Isaac Sim, ROS) can easily consume **15 GB to 50+ GB each**.  
    To avoid filling up the shared 1 TB NVMe SSD with redundant environments:
    
    1. **Check the registry below** and run `docker images` on the server before building or pulling a new Docker image.
    2. Whenever possible, **reuse or extend an existing image** instead of creating a new one from scratch.
    3. **Register your images**: If you build or pull a new image intended for shared or repeated use, **please add a row to this table** so other researchers know it is available.

#### Available Images on the Server

| Image Name & Tag | Base Stack | Contents & Key Libraries | Maintainer / Contact | Primary Purpose |
|---|---|---|---|---|
| `isaac-sim:4.2.0` | Ubuntu 22.04 + CUDA 12.2 | Isaac Sim 4.2.0 runtime, Omniverse Kit, Python 3.10 | [Administrators](administrators.md) | Graphical robotics simulation, WebRTC livestreaming (`isaacsim`) |
| `isaac-lab:latest` | Ubuntu 22.04 + Isaac Sim 4.2.0 | Isaac Lab, PyTorch, RSL-RL, RL-Games, Gymnasium | [Administrators](administrators.md) | Reinforcement learning and robot learning pipelines (`isaaclab`) |
| *`<your-image>:<tag>`* | *e.g. Ubuntu 22.04 + CUDA 12.4* | *e.g. PyTorch 2.5, Torchvision, HuggingFace, OpenCV* | *[Your Name / Contact]* | *[Brief description of project/purpose]* |

#### How to Add Your Image to the Table

To keep this catalog up to date for the entire lab:
1. Ensure your image has a clear, descriptive repository name and version tag on the host (e.g. `docker tag <image_id> lab-<framework>:<version>`).
2. Open this documentation file ([`docs/robots/server/server_workstation.md`](server_workstation.md)) and append a new row to the table above.
3. Include the image tag, base stack, main libraries, your name/contact, and primary purpose.
4. Commit and push the changes (or submit a pull request) so other members can see and reuse the image.

#### Useful Docker Image Inspection Commands

```bash
# List all Docker images currently stored locally on the workstation
docker images

# Check total disk space consumed by Docker (images, containers, build cache)
docker system df

# Remove dangling, untagged images (<none>) safely
docker image prune
```

---

## Available Server Guides

| Guide | Description |
|---|---|
| [Isaac Sim & Isaac Lab](isaac_sim_lab.md) | Comprehensive manual for launching NVIDIA Isaac Sim and Isaac Lab via `isaacsim` and `isaaclab`, WebRTC streaming, folder mounting, and troubleshooting. |
| [System Administrators](administrators.md) | Contact information for account creation, Docker group permissions, software installation requests, and lab communication channels. |

---

## Local Python Execution (Host Environment)

Whenever possible, execute your workflows inside containers. If you strictly need to execute Python scripts directly on the host machine:

- System `pip` is **not available** on the host to preserve system package integrity.
- Use [**uv**](https://docs.astral.sh/uv/) to manage isolated virtual environments and install packages.

### Creating and Activating Virtual Environments with `uv`

Create and activate a virtual environment in your project directory:

```bash
uv venv .venv
source .venv/bin/activate
uv pip install <package>
```

### Running Scripts Without Manual Activation

You can execute a Python script directly within a managed environment without activating it:

```bash
uv run script.py
```

!!! warning "Host Environment Limitations"
    Host-level execution is meant for **small, occasional utility tasks only**. For long-running experiments, simulations, or training jobs, **using Docker is always required**.

---

## Remote Execution & Persistent Jobs with `tmux`

When connecting to the workstation via SSH, any command running directly in your terminal will **terminate immediately** if the network connection drops (e.g. Wi-Fi disconnection, closed laptop lid, SSH timeout) or if you close the terminal window.

To submit long-running simulations, model training runs, or batch tasks without remaining perpetually connected, use [**tmux**](https://github.com/tmux/tmux/wiki) (terminal multiplexer). A `tmux` session keeps processes alive in an independent background session on the server, allowing you to safely disconnect and reattach at any time.

### Basic `tmux` Workflow

#### 1. Start a New Named Session
Before launching your job, create and attach to a new session:

```bash
tmux new -s <session_name>
```

*(e.g. `tmux new -s training_run`)*

#### 2. Launch Your Workload Inside the Session
Inside the session, run your Docker container, simulation, or training script as usual:

```bash
isaaclab python scripts/reinforcement_learning/rsl_rl/train.py --task Isaac-Cartpole-Direct --headless
```

#### 3. Detach from the Session
To leave the job running safely in the background:
- Press `Ctrl + B`, release both keys, then press `D`.
- You will be returned to your normal shell prompt with a confirmation message (e.g. `[detached (from session training_run)]`).
- You can now safely close your terminal or log out of SSH (`exit`).

#### 4. Reattach to an Existing Session
When you log back into the workstation over SSH, list and reconnect to your session:

```bash
# List all active sessions
tmux ls

# Reattach to your session
tmux attach -t <session_name>
# (shortcut: tmux a -t <session_name>)
```

#### 5. Terminate the Session When Finished
Once your training or simulation finishes:
- Inside the session: type `exit` or press `Ctrl + D`.
- From outside the session:
```bash
tmux kill-session -t <session_name>
```

### Essential `tmux` Shortcuts

All shortcuts require pressing the prefix combination **`Ctrl + B`**, releasing it, and then pressing the desired key:

| Shortcut | Description |
|---|---|
| `Ctrl + B`, then `d` | **Detach** from the active session (process keeps running in the background) |
| `Ctrl + B`, then `[` | Enter **scrollback / navigation mode** (scroll using arrow keys or `PageUp`/`PageDown`; press `q` to exit) |
| `Ctrl + B`, then `c` | Create a new window within the current session |
| `Ctrl + B`, then `n` / `p` | Switch to the next / previous window |
| `Ctrl + B`, then `"` | Split window into horizontal panes |
| `Ctrl + B`, then `%` | Split window into vertical panes |
| `Ctrl + B`, then `o` | Cycle between split panes |

---

## Experiment Tracking & Remote Monitoring

### Persistent Logging with `tee`

Inside `tmux`, long-running training jobs output thousands of lines. If a terminal buffer rolls over or a session is closed unintentionally, output printed only to stdout will be lost.

Always redirect both standard output and standard error simultaneously to the terminal and a persistent log file using `tee`:

```bash
# Example training command with date-stamped log file
isaaclab python scripts/reinforcement_learning/rsl_rl/train.py --headless 2>&1 | tee train_$(date +%Y%m%d_%H%M%S).log
```

- `2>&1`: Merges standard error into standard output so errors and stack traces are captured.
- `| tee <file>`: Displays real-time terminal output while safely streaming everything to disk.

### Remote TensorBoard via SSH Port Forwarding

You do not need an active graphical window or remote desktop session to view TensorBoard or metric dashboards. You can forward the web interface directly to your local laptop browser via SSH:

1. **Establish an SSH Tunnel on your local laptop**:
   ```bash
   ssh -L 6006:localhost:6006 <username>@<workstation-ip>
   ```
2. **Start TensorBoard on the workstation** (or inside your container):
   ```bash
   tensorboard --logdir=/workspace/runs --port=6006
   ```
3. **Open the dashboard locally**:  
   Open your laptop's browser and navigate to `http://localhost:6006`. All graphs and metrics render locally without streaming high-bandwidth desktop video.

---

## Resource Monitoring & Handling Orphaned Processes

### Monitoring GPU and System Resources

Before submitting heavy computational jobs, check resource utilization to avoid interfering with ongoing runs:

- **GPU Utilization & VRAM**:
  ```bash
  watch -n 1 nvidia-smi
  ```
  Look for GPU temperature, VRAM usage (e.g. `18420MiB / 24564MiB`), and active compute processes.
- **CPU, Memory, and Disk I/O**:
  ```bash
  btop
  ```

### Reclaiming VRAM from Orphaned Processes & Containers

If an experiment crashes, or if an SSH session disconnects without a proper exit, background Python processes or Docker containers may continue holding onto GPU memory (**zombie/orphaned processes**):

1. **List running containers**:
   ```bash
   docker ps
   ```
2. **Stop your crashed or orphaned container**:
   ```bash
   docker stop <container_id_or_name>
   ```
3. **Find processes holding the NVIDIA GPU**:
   If `nvidia-smi` shows allocated VRAM but no running container matches, check which process IDs (PIDs) are attached to the GPU devices:
   ```bash
   fuser -v /dev/nvidia*
   ```
4. **Terminate stuck processes safely**:
   Inspect the process owner before terminating it:
   ```bash
   ps -u <PID>
   ```
   !!! caution "Do Not Kill Others' Processes"
       Only kill processes belonging to your user account. Terminating another user's active job will result in lost experimental progress. If you suspect an orphaned process belongs to another user, coordinate via the [WhatsApp Group](administrators.md#communication--lab-community).

---

## Storage Architecture & Disk Usage Policy

The workstation is equipped with two internal storage drives optimized for different stages of development and training:

| Drive Type | Capacity | Performance | Intended Purpose |
|---|---|---|---|
| **Fast NVMe SSD** | **1 TB** | Ultra-high read/write throughput, low latency | **Active workloads only**: Operating system, Docker images, and datasets actively used during an ongoing training run. |
| **Slower SATA Drive** | **2 TB** | Standard speed, larger capacity | **Staging & long-term storage**: Master datasets, raw data archives, pre-trained baselines, historical checkpoints, and inactive projects. |

### Fair-Share Disk Policy

Because the 1 TB NVMe SSD is shared among all lab members and also hosts the operating system and Docker runtime, **free space on the NVMe drive is strictly limited**. If the NVMe drive fills up, running training jobs will fail and system services may crash.

To respect shared resources and maintain workstation stability, all users must follow these rules:

1. **Temporary Data Residency on NVMe**:  
   Datasets must reside on the fast 1 TB NVMe drive **only for the active duration of the training run**.
2. **Stage on SATA, Train on NVMe, Clean Up Immediately**:  
   - **Before Training**: Keep your primary dataset files and archives on the 2 TB SATA drive. Copy or symlink only the necessary subset to your NVMe workspace immediately before launching training.
   - **After Training**: As soon as your training run completes, transfer generated artifacts (model weights, checkpoints, logs, evaluation videos) to the 2 TB SATA drive (or your personal storage) and **immediately delete or remove the dataset copy from the NVMe disk**.
3. **No Inactive Dataset Parking**:  
   Do not leave inactive datasets, cached intermediate features, or old checkpoints parked on the 1 TB NVMe drive while waiting days or weeks between experiments.
4. **Check Your Disk Consumption**:  
   Check disk usage regularly and ensure you are not exhausting partition space:
   ```bash
   # Inspect free space on mounted partitions
   df -h

   # Inspect disk consumption of your directories
   du -sh ~/projects/* | sort -h
   ```

---

## Student Workflow: End-to-End Training Checklist

Follow this 5-step checklist whenever you run an experiment on the workstation:

```text
[1] Pre-Flight Checks
    ├── Check GPU availability: nvidia-smi
    ├── Check free disk space: df -h
    └── Check Docker Registry for existing images

[2] Data Staging
    └── Copy/symlink active dataset slice from SATA (2 TB) to NVMe (1 TB)

[3] Launch Workload in tmux
    ├── Start session: tmux new -s <experiment_name>
    ├── Run inside Docker with logging: ... 2>&1 | tee train.log
    └── Detach safely: Ctrl + B, then D

[4] Remote Monitoring
    ├── Reattach when needed: tmux attach -t <experiment_name>
    └── Monitor metrics locally: ssh -L 6006:localhost:6006 ...

[5] Post-Training Cleanup
    ├── Move checkpoints, models, and logs to SATA (2 TB)
    ├── Delete temporary datasets and cache from NVMe (1 TB)
    └── Close tmux session (exit) and verify GPU memory freed
```

---

## Best Practices & Workspace Organization

1. **Follow the training checklist**: Run through the [Student Workflow Checklist](#student-workflow-end-to-end-training-checklist) for every experiment.
2. **Keep projects in your home directory**: Store your code and datasets inside your user space (e.g. `~/projects/...`).
3. **Check the Docker registry first**: Before pulling or building new images, inspect the [Docker Images Registry](#shared-docker-images-registry) to reuse existing environments and preserve NVMe disk space.
4. **Adhere to the disk policy**: Keep long-term data on the 2 TB SATA drive and utilize the 1 TB NVMe drive only during active training runs.
5. **Run background jobs in `tmux`**: Always run long experiments or simulations inside a detached `tmux` session to prevent jobs from dying upon SSH disconnection.
6. **Mount only what you need**: When using containerized tools, mount specific project folders into the container rather than your entire home directory.
7. **Coordinate heavy workloads**: Verify GPU and CPU availability using `nvidia-smi` and `btop` before launching intensive training jobs.
8. **Need help or permissions?**: Refer to the [System Administrators](administrators.md) page for support.
