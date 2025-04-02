# OSAI Demo Infrastructure

An Ansible-driven infrastructure template to deploy and validate an on-prem stack consisting of:

- 🧠 **Qdrant** — a high-performance vector database (Docker-based)
- 🔌 **Vatrix Receiver** — a FastAPI endpoint for Vatrix NLP Processor
- 🔌 **Vatrix Gateway** — a FastAPI-based API for Vatrix NLP Processor (Docker-based)
- 🧪 **Post-install test script** to validate end-to-end vector indexing and search

---

## ⚙️ Requirements

- Ubuntu 20.04+ (tested on 20.04)
- SSH access with `sudo` privileges
- Python 3.8+ installed on the control node
- Ansible 2.12+ on the control node

---

## 🗺 Inventory Setup

Edit `inventory/hosts.ini` with your target host:

```ini
[qdrant]
lan-test ansible_host=192.168.1.1 ansible_user=ubuntu

[vatrix]
lan-test ansible_host=192.168.1.1 ansible_user=ubuntu

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

---

## 🚀 Deploying the Stack

```bash
make deploy
```

This will:
- Install Docker
- Deploy Qdrant as a container on port 6333
- Set up Vatrix under /opt/vatrix with a virtualenv and systemd unit on port 8000
- Validate Qdrant is healthy
- Install Docker & Dependencies
- Deploy Qdrant as a container on port 6334
- Build Vatrix Gateway
- Set up Vatrix Gateway as a container on port 8000
- Validate stack is healthy
- Tests /ingest and /search APIs

---

## 🧪 Running the Post-Install Test

```bash
make test
```

This will:
- Wait for Vatrix (FastAPI) to become available
- Wait for Vatrix Gateway to become available
- Push a synthetic 384-dim vector to Qdrant
- Search and return the result

---

## 🔁 Tearing Down
To fully clean up all deployed services and files:

```bash
make destroy
```

This removes:
- Qdrant container and image
- Vatrix app, logs, virtualenv, and systemd unit
- Vatrix Gateway container and image

---

## 📦 Project Structure

```bash
osai-demo/
├── playbook.yml           # Main deployment entrypoint
├── teardown.yml           # Full stack teardown
├── inventory/             # Hosts and variable overrides
├── roles/                 # Ansible roles (deploy + teardown)
├── scripts/
```

---

## 🛠 Future Plans

- Dockerize Vatrix for full container parity
- TLS/Nginx reverse proxy for hardened deployments
- make deploy / make destroy CLI workflow
- Pro edition features (auth, cloud support, etc.)

---

## 📚 License

MIT © Brian Bates

Built with ❤️, caffeine, and curiosity.