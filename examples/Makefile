TARGET_IP?=192.168.2.143
TARGET_USER=pi
TARGET_EXAMPLE_DIR=/home/${TARGET_USER}/lcd-screen-piface/examples

.PHONY: env
env:
	virtualenv .venv -p /usr/bin/python3 && . .venv/bin/activate && python -m pip install -r requirements.txt

.PHONY: deploy
deploy:
	echo "Deploying" && ssh $(TARGET_USER)@$(TARGET_IP) "rm -rf $(TARGET_EXAMPLE_DIR)" && ssh $(TARGET_USER)@$(TARGET_IP) "mkdir -p $(TARGET_EXAMPLE_DIR)" && scp -r ./* $(TARGET_USER)@$(TARGET_IP):$(TARGET_EXAMPLE_DIR)

.PHONY: run-pager
run-pager:
	echo "Run the pager" && . .venv/bin/activate && cd pager && python pager_example.py
