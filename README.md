![Python](https://img.shields.io/badge/python-3.8-blue)  ![License](https://img.shields.io/badge/license-MIT-green) [![Last Commit](https://img.shields.io/github/last-commit/brianbatesactual/OSAI-Demo)](https://github.com/brianbatesactual/vatrix) [![Stars](https://img.shields.io/github/stars/brianbatesactual/vatrix?style=social)](https://github.com/brianbatesactual/OSAI-Demo)

# OSAI Demo Infrastructure

An Ansible-driven infrastructure template to deploy and validate an on-prem stack consisting of:

- 🧠 **Qdrant** — a high-performance vector database (Docker-based)
- 🔌 **Vatrix Gateway** — a FastAPI endpoint for Vatrix NLP Processor
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

[vatrix_gateway]
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
- Set up Vatrix Gateway under /opt/vatrix_gateway with a virtualenv and systemd unit on port 8000
- Validate Qdrant is healthy

---

## 🧪 Running the Post-Install Test

```bash
make test
```

This will:
- Wait for Vatrix Gateway (FastAPI) to become available
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
- Vatrix Gateway, logs, virtualenv, and systemd unit

---

## 📦 Project Structure

```bash
osai-demo/
├── playbook.yml           # Main deployment entrypoint
├── teardown.yml           # Full stack teardown
├── inventory/             # Hosts and variable overrides
├── roles/                 # Ansible roles (deploy + teardown)
├── scripts/test_post_install.sh
```

---

## 🛠 Future Plans

- Dockerize Vatrix Gateway for full container parity
- TLS/Nginx reverse proxy for hardened deployments
- make deploy / make destroy CLI workflow
- Pro edition features (auth, cloud support, etc.)
- ⚠️ Stack uses docker-compose file format 3.3 for compatibility with older Docker Compose versions. You may upgrade to 3.9+ with the newer docker compose CLI plugin.

---

## 📚 License

MIT © Brian Bates

Built with ❤️, caffeine, and curiosity.