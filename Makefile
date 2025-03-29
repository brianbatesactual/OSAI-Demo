# Makefile for osai-demo

.PHONY: deploy destroy test logs

deploy:
	ansible-playbook -i inventory/hosts.ini playbook.yml --ask-become-pass

destroy:
	ansible-playbook -i inventory/hosts.ini teardown.yml --ask-become-pass

test:
	./scripts/test_post_install.sh