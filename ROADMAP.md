# Roadmap

## Current Status

- Local Mosquitto broker running in Docker
- Basic Python publisher and subscriber using Paho MQTT
- Virtual environment, dependency file, and startup script
- Initial project versioned on GitHub

## Next Steps

1. Add JSON payload parsing and validation
2. Create multiple clients and use wildcard subscriptions
3. Separate telemetry, command, and device-status topics
4. Compare the same Python clients with HiveMQ and Mosquitto
5. Add QoS, reconnect handling, and Last Will and Testament
6. Add logging, tests, configuration, and documentation
7. Make the broker setup reproducible with Docker Compose

## Scope

The project evolves through small, independent MQTT clients. Each new capability is implemented as a new publisher, subscriber, or client that performs both roles, while earlier examples remain available for reference.
