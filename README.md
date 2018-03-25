# Xioami Mi WiFi Repeater 2

This is a custom component for home assistant to integrate the Xioami Mi WiFi Repeater 2.

Please follow the instructions on [Retrieving the Access Token](https://home-assistant.io/components/xiaomi/#retrieving-the-access-token) to get the API token to use in the configuration.yaml file.

Credits: Thanks to [Rytilahti](https://github.com/rytilahti/python-miio) for all the work.

## Setup

```yaml
# confugration.yaml

device_tracker:
  - platform: xiaomi_miio
    host: 192.168.130.73
    token: 56197337f51f287d69a8a16cf0677379
```

Configuration variables:
- **host** (*Required*): The IP of your wifi repeater.
- **token** (*Required*): The API token of your wifi repeater.
