# Systemd

### Create a new systemd service file
sudo nano /etc/systemd/system/yourapp.service

### The minimum service definition for the service
[Unit]
Description=Your App Name
After=network.target

[Service]
User=devin
WorkingDirectory=/path/to/your/app
ExecStart=/path/to/your/venv/bin/python server.py
Restart=always

[Install]
WantedBy=multi-user.target

### Additional parameters to use in the standard service file

EnvironmentFile=/path/to/your/app/.env
RestartSec=3
Environment=PYTHONUNBUFFERED=1

### Commands used with systemd

Once a new systemd file has been created, run the following command to pick up the new file.

`sudo systemctl daemon-reload`

Once the file has been picked up, run the following command to enable your app so that it starts on boot.

`sudo systemctl enable yourapp`

Once your app has been enabled, run the following command to start the app.

```bash
sudo systemctl start yourapp
```

You can check if the app is running with the following command.

`sudo systemctl status yourapp`

Lastly, after you have made code changes to your app, run the following command to pick them up.

`sudo systemctl restart yourapp`