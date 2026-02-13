# Cloudflare

When adding a new domain or subdomain to the server, you need to add it to the Cloudflar configuration file.

`sudo nano /etc/cloudflared/config.yml`

The simple pattern for the file is the following. Add it above the catch-all 404.

  - hostname: sandbox.devinmarch.com
    service: http://localhost:80

Then you have to route DNS through the Cloudflare tunnel by using the following command.

`sudo cloudflared tunnel route dns devin-server sandbox.devinmarch.com`

Once this is successful, restart the cloudflard service with the following command.

`sudo systemctl restart cloudflared`

