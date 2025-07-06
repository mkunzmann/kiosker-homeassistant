# Kiosker Home Assistant Integration

This integration allows you to control and monitor devices running [Kiosker](https://kiosker.io) from Home Assistant.

## Features
- Send navigation commands to your Kiosker device (e.g., open a specific dashboard)
- Monitor device status and key metrics as Home Assistant sensors
- Button entity to trigger navigation to a Home Assistant dashboard

## Requirements
- Your device must be running Kiosker with a valid subscription or the PRO version, as only these versions support the REST API required by this integration.
- The Kiosker REST API must be enabled and accessible from your Home Assistant instance.

## Setup
1. Install this custom integration in your Home Assistant `custom_components` directory.
2. Add the integration via the Home Assistant UI and provide your device's IP address, token, and other required details.
3. Once configured, you can use the provided sensors and button entity to interact with your Kiosker device.

## Notes
- For more information about Kiosker and its features, visit [kiosker.io](https://kiosker.io).
- If you do not have a subscription or the PRO version, the REST API will not be available and this integration will not function.