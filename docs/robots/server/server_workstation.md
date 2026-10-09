# Lab Workstation – Overview and General Usage

The Prisma Lab workstation is a shared high-performance compute machine dedicated to physics simulation, robot learning, model training, and heavy computational tasks.

---

## Architecture & Container-First Principle

!!! tip "Always Prefer Docker"
    Whatever workload or experiment you need to run on the workstation, **always run it inside a Docker container**.  
    Running containerized environments keeps the host operating system clean, avoids package version conflicts across users, and guarantees reproducible experimental setups.

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

## Best Practices & Workspace Organization

1. **Keep projects in your home directory**: Store your code and datasets inside your user space (e.g. `~/projects/...`).
2. **Mount only what you need**: When using containerized tools, mount specific project folders into the container rather than your entire home directory.
3. **Coordinate heavy workloads**: Verify GPU and CPU availability using `nvidia-smi` and `btop` before launching intensive training jobs.
4. **Need help or permissions?**: Refer to the [System Administrators](administrators.md) page for support.
