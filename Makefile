# Makefile for osai-demo

enable_nginx ?= false

.PHONY: deploy destroy test logs

deploy:
	ansible-playbook -i inventory/hosts.ini playbook.yml --ask-become-pass --extra-vars "enable_nginx=$(enable_nginx)"

destroy:
	ansible-playbook -i inventory/hosts.ini teardown.yml --ask-become-pass

test:
	./scripts/test_post_install.sh