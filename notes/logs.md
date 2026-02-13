# Server logs

In order to watch your specific apps logs use the following command.

`sudo journalctl -u yourapp -f`

If you would like to view logs with recent history you can use.

`sudo journalctl -u yourapp -f --since "5 minutes ago"`