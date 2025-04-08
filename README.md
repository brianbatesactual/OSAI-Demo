![Python](https://img.shields.io/badge/python-3.8-blue)  ![License](https://img.shields.io/badge/license-MIT-green) [![Last Commit](https://img.shields.io/github/last-commit/brianbatesactual/OSAI-Demo)](https://github.com/brianbatesactual/vatrix) [![Stars](https://img.shields.io/github/stars/brianbatesactual/vatrix?style=social)](https://github.com/brianbatesactual/OSAI-Demo)

# OSAI Demo Infrastructure

An Ansible-driven infrastructure template to deploy and validate an on-prem stack consisting of:

- 🧠 **Qdrant** — a high-performance vector database (Docker-based)
- 🔌 **Vatrix Gateway** — a FastAPI-based API for Vatrix NLP Processor (Docker-based)
- 🌐 **NGINX** - a reverse proxy in front of Vatrix Gateway (optional)
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

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

---

## 🚀 Deploying the Stack

```bash
make deploy
```

This will:
- Install Docker & Dependencies
- Deploy NGINX as a container on port 80 (optional: "make deploy enable_nginx=true")
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
- Wait for NGINX to become available, if enabled
- Test for Vatrix Gateway to be available
- Push a synthetic 384-dim vector to Qdrant
- Search and return the result

---

## 🔁 Tearing Down
To fully clean up all deployed services and files:

```bash
make destroy
```

This removes:
- NGINX container and image (if applicable)
- Qdrant container and image
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

- make deploy / make destroy CLI workflow
- Pro edition features (auth, cloud support, etc.)
- ⚠️ Stack uses docker-compose file format 3.3 for compatibility with older Docker Compose versions. You may upgrade to 3.9+ with the newer docker compose CLI plugin.

---

## 📚 License

MIT © Brian Bates

Built with ❤️, caffeine, and curiosity.