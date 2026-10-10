# Isaac Sim and Isaac Lab – Workstation Operation Guide

This guide explains how to use **NVIDIA Isaac Sim** and **Isaac Lab** on the shared lab workstation.

You do not need detailed knowledge of Docker internals: simulation and training environments are accessed via two dedicated commands: `isaacsim` and `isaaclab`.

Whenever this guide mentions contacting the administrators, consult the [System Administrators](administrators.md) page.

---

## Architecture & Container Lifecycle

- **Pre-installed containers**: Isaac Sim and Isaac Lab are installed once on the workstation inside dedicated Docker containers with full NVIDIA GPU support.
- **Isolated per-user environments**: Whenever you execute a command, your personal container starts. Multiple team members can work simultaneously without interfering with each other's workspaces.
- **Ephemeral container storage**: When you exit the container, the container instance is **deleted**. Only the following resources are preserved across runs:
    1. Your mounted **project folders** (see [Connecting Workspaces & Folders](#connecting-workspaces-folders));
    2. Your personal **cache and configuration directory**: `~/docker/isaac-sim/`;
    3. **Packages and extensions** installed inside the container using `pip install --user`.

!!! warning "Data Persistence Notice"
    **Any file created outside your mounted project folders or personal cache is lost when you exit the container.**  
    Always store training checkpoints, models, datasets, logs, and video recordings inside your project directories under `/workspace/`.

### Core Commands

| Command | Purpose | Typical Use Case |
|---|---|---|
| `isaacsim` | Isaac Sim runtime environment | Opening the Isaac Sim graphical interface, WebRTC livestream, or running standalone scripts |
| `isaaclab` | Isaac Lab learning framework | Launching reinforcement learning training runs, framework scripts, and interactive shells |

---

## First-Time Setup

### 1. Verify Docker Permissions

Verify that your user account has access to the Docker daemon by running:

```bash
groups
```

`docker` must appear in the output. If it does not appear, ask a [system administrator](administrators.md) to add you to the `docker` group, then log out and log back in.

### 2. Configure Directory Mounts

The container does not expose your entire file system automatically; you must explicitly configure which folders to link. Generate your personal configuration:

```bash
mkdir -p ~/.config/isaac
cp /usr/local/share/doc/isaac-docker/mounts.example ~/.config/isaac/mounts
nano ~/.config/isaac/mounts
```

Add your project folders, one per line (see [Connecting Workspaces & Folders](#connecting-workspaces-folders)).

### 3. Launch Initial Run

Launch either `isaacsim` or `isaaclab`.

!!! note "Initial Shader Compilation"
    The very first launch takes **10 minutes or more** because Isaac Sim must compile its internal shader cache. All subsequent launches will start significantly faster.

---

## Connecting Workspaces & Folders

Inside the container, all connected folders are mounted under **`/workspace/`**.

### Permanent Mounts: `~/.config/isaac/mounts`

Specify one folder per line using the following syntax:

```text
path_on_the_machine[:name][:ro]
```

**Example configuration:**

```text
# Lines starting with # are comments
~/projects/drone_controller
~/datasets/flights:flights:ro
```

| Line | In-Container Path | Notes |
|---|---|---|
| `~/projects/drone_controller` | `/workspace/drone_controller` | The destination folder inherits the host folder name. |
| `~/datasets/flights:flights:ro` | `/workspace/flights` | `ro` = **read-only**: container processes cannot modify or delete files. |

**Mount guidelines:**
- Use the `:ro` flag for datasets, pretrained baselines, and reference assets to prevent accidental loss.
- Custom folder alias names may only contain alphanumeric characters, `.`, `-`, and `_`.
- The identifier `isaaclab` is reserved internally.

### Temporary Mounts for Single Runs: `-v` Flag

To attach a folder for a single command invocation without modifying your `mounts` configuration file:

```bash
isaaclab -v ~/tests/quick_test
isaacsim -v ~/data/scenes:scenes:ro
```

---

## Using `isaacsim`

The `isaacsim` command manages the NVIDIA Isaac Sim environment.

| Command | Function |
|---|---|
| `isaacsim` | Opens Isaac Sim (automatically determines the appropriate display mode). |
| `isaacsim -H` | Forces WebRTC livestream mode (even when working at the physical workstation monitor). |
| `isaacsim -s` | Launches an interactive bash shell inside the container. |
| `isaacsim ./python.sh /workspace/project/script.py` | Executes a custom Python script using Isaac Sim's internal runtime. |
| `isaacsim -h` | Displays help and command options. |

### Display Mode Selection & Remote Livestreaming

When `isaacsim` is run without extra flags, it detects the active session type:

- **Physical Workstation Session** (sitting at the lab monitor):  
  The Isaac Sim graphical window opens directly on the display.
- **Remote SSH Session**:  
  Isaac Sim starts without a local window and streams video output over the network (**livestream**).  
  To view and control the simulator:
  1. Install the **Isaac Sim WebRTC Streaming Client** on your local computer.
  2. Enter the workstation's IP address and port in the client.
  3. Wait until the message `Isaac Sim Full Streaming App is loaded.` appears in your SSH terminal, then click **Connect**.

!!! warning "Livestream Concurrency Limitation"
    The WebRTC livestream can be used by **only one person at a time** on the entire workstation. If the port is in use, coordinate with the active user.

!!! note "SSH X11 Forwarding Notice"
    Connecting via `ssh -X` or `ssh -Y` does **not** allow opening the Isaac Sim window, as NVIDIA Omniverse requires direct hardware acceleration. For remote access, use WebRTC livestream or headless execution.

---

## Using `isaaclab`

The `isaaclab` command launches the Isaac Lab framework for reinforcement learning and robot learning tasks.

| Command | Function |
|---|---|
| `isaaclab` | Opens an interactive bash shell in the Isaac Lab folder inside the container. |
| `isaaclab python <script> ...` | Runs an Isaac Lab Python script. |
| `isaaclab pip ...` | Uses `pip` inside the container environment. |
| `isaaclab -h` | Displays help and available flags. |

Inside the container, `python` and `pip` are pre-configured to use Isaac Sim's Python environment; no virtual environment activation is needed.

### Launching Training Runs

To launch a reinforcement learning task:

```bash
isaaclab python scripts/reinforcement_learning/rsl_rl/train.py --task Isaac-Cartpole-Direct --headless
```

- Always use `--headless` when connected through SSH to avoid display errors.
- If working directly at the physical workstation monitor, omit `--headless` to watch the simulation live.
- Relative paths (such as `scripts/...`) resolve from the root of the Isaac Lab repository. For your own scripts, use absolute paths within the container (e.g. `/workspace/my_project/train.py`).

!!! tip "Persistent Background Sessions with `tmux`"
    Training runs will stop if your SSH terminal session disconnects. Run persistent tasks inside a multiplexer such as `tmux` or `screen` on the workstation:
    ```bash
    tmux new -s my_training
    isaaclab python scripts/... --headless
    # Detach with: Ctrl + B, then D
    # Reattach later with: tmux attach -t my_training
    ```
    For a full guide on `tmux` workflows and shortcuts, see the [Lab Workstation Overview](server_workstation.md#remote-execution--persistent-jobs-with-tmux).

### Developing with Custom Isaac Lab Projects

If you have a project created from the Isaac Lab template, install it in editable mode inside the container so the framework can discover your tasks:

```bash
isaaclab pip install --user -e /workspace/my_project/source/my_project
```

- This operation only needs to be performed **once**: because packages installed with `--user` are stored persistently, the installation persists across container restarts.
- Thanks to `-e` (editable mode), code updates on the host are reflected immediately without reinstalling.
- Re-installation is only required if the system administrator upgrades the underlying Isaac Lab container image.

---

## Attaching a Secondary Terminal to a Running Container

If a training job or simulation is currently running and you need to access the active container to inspect files or run diagnostics:

Open a new terminal window on the workstation and run:

| Running Process | Secondary Command |
|---|---|
| `isaaclab` | `isaaclab` |
| `isaacsim` | `isaacsim -s` |

This attaches directly into the **already running container** without interrupting the ongoing task.

---

## Operational Rules & Resource Sharing

1. **Mutual exclusion**: You cannot run `isaacsim` and `isaaclab` simultaneously under your user account. Both tools share the Omniverse kit cache, and concurrent execution will corrupt it. Stop one command before starting the other.
2. **GPU resource sharing**: The workstation has a single shared GPU. Multiple users can work simultaneously, but concurrent heavy training runs will reduce throughput for everyone. Check GPU utilization (`nvidia-smi`) and coordinate compute-heavy jobs.
3. **Disk usage policy**: High-speed NVMe space is shared and limited. Store datasets on the 1 TB NVMe drive only for the duration of the active training run, and move or delete them once completed (see [Storage Policy](server_workstation.md#storage-architecture--disk-usage-policy)).
4. **Closing containers**: To terminate an active session, close the graphical window, send `Ctrl + C` in the terminal, or type `exit` in an interactive shell.

---

## Troubleshooting & Diagnostics

| Error / Message | Meaning | Recommended Action |
|---|---|---|
| `permission denied ... docker.sock` | You are not in the `docker` user group. | Ask a [system administrator](administrators.md) to add you. |
| `mount path not found: ...` | A path specified in the configuration does not exist. | Check and correct paths in `~/.config/isaac/mounts`. |
| `invalid workspace name: ...` | Folder name contains forbidden characters. | Use only letters, numbers, `.`, `-`, and `_`. |
| `... is already running` | Your container is already active. | Attach using a secondary terminal or terminate the existing run. |
| `... shares the kit cache, stop it first` | The other command is already running. | Close the running command before starting the next one. |
| `port 49100 busy` | Another user is using the WebRTC livestream. | Wait until the current user completes their session. |
| `'setfacl' not found` / `'xauth' not found` | Required host utility is missing. | Contact an administrator to install the missing package. |
| `Permission denied` inside the container | Writing outside your mounted workspaces. | Save data under `/workspace/...`. If the problem persists, notify an administrator. |
| Multiple `OmniHub ... Trying to reconnect to Hub` warnings | Normal Omniverse hub connection check. | Safe to ignore; clears after ~10 seconds. |
| Very slow first startup | Initial shader compilation. | Normal behavior on first launch; subsequent runs will be fast. |
| Livestream starts while at the physical workstation | Display detection failure. | Send the output of `echo $DISPLAY; ls /tmp/.X11-unix` to an administrator. |
| Startup crash or abnormal configuration errors | Corrupted shader or kit cache. | Clear cache (see instructions below). |

### Clearing the Cache

If Isaac Sim crashes unexpectedly on startup or displays corrupted settings, clear the cache and configuration folders:

```bash
rm -rf ~/docker/isaac-sim/cache ~/docker/isaac-sim/config
```

The next launch will take longer to compile shaders, but will start from a clean state. If `rm` returns permission errors, contact a [system administrator](administrators.md).
