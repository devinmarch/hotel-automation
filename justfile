# Commit script
commit *msg:
	git add . && git commit -m "{{msg}}" && git push

# Restart systemd for sandbox
restart:
	sudo systemctl restart hotel-automation

# Start the local server
start:
	python server.py

# Start a Tailscale funnel
tailfun:
	tailscale funnel 5003

# CloudBeds webhook registration tool
cbweb:
	python notes/tools/cb_webhook_tool.py

# Run sync function to save to db
sync:
	python sync.py
