TARGET_IP=192.168.1.68
TARGET_USER=pi
TARGET_EXAMPLE_DIR=/home/${TARGET_USER}/lcd-screen-piface/

.PHONY: env
env:
	virtualenv venv --no-site-packages -p /usr/bin/python3 && . venv/bin/activate && python -m pip install -r requirements.txt

.PHONY: deploy
deploy_examples:
	ssh $(TARGET_USER)@$(TARGET_IP) "rm -rf $(TARGET_EXAMPLE_DIR)" && ssh $(TARGET_USER)@$(TARGET_IP) "mkdir -p $(TARGET_EXAMPLE_DIR)" && scp pager_example.py $(TARGET_USER)@$(TARGET_IP):$(TARGET_EXAMPLE_DIR) && scp -r pager $(TARGET_USER)@$(TARGET_IP):$(TARGET_EXAMPLE_DIR)
