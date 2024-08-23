# 🚓 ERLC API Wrapper 🚒

![License](https://img.shields.io/github/license/AJXD2/erlc-api)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

Welcome to the **ERLC API Wrapper** – your go-to Python library for interacting with the **Emergency Response: Liberty County** API. Whether you're building bots, dashboards, or integrating with other systems, this wrapper makes it effortless to retrieve and manipulate game data.

## ✨ Features

- 🚀 **User-Friendly**: Simplified functions for every endpoint.
- 🌐 **Complete Coverage**: Access every available API endpoint with ease.
- ⚡ **Robust Error Handling**: Thoughtful error management to keep your app running smoothly.

## 📦 Installation

Although this package isn't on PyPI yet, you can still get started by cloning the repository:

```bash
git clone https://github.com/AJXD2/erlc-api.git
cd erlc-api
poetry install
```

Make sure you have [Poetry](https://python-poetry.org/docs/#installation) installed to manage dependencies.

## 🛠️ Usage

Dive right in with this sample code to see how the wrapper works:

```python
from erlc import ErlcClient

client = ErlcClient()
server = client.get_server("...")

# 🚓 Get Server Info
print(server)

# 🔍 Explore Join Logs
print(server.joinlogs)

# 💥 Retrieve Kill Logs
print(server.killlogs)

# 🛡️ Access Command Logs
print(server.commandlogs)

# 🚨 View Mod Calls
print(server.modcalls)

# 🚷 Check Bans
print(server.bans)

# ⏳ See Queue
print(server.queue)

# 👥 List Players
print(server.players)

# 🚗 Get Vehicles
print(server.vehicles)

# 💻 Run commands
server.run_command(":m Hello World!")

```

This is just a glimpse of what you can do! Whether you're managing a server or simply exploring the data, this wrapper has you covered.

## 📚 API Reference

For full details on all the available endpoints, take a look at the [official ERLC API documentation](https://apidocs.policeroleplay.community/).

## 🤝 Contributing

Have an idea? Found a bug? Contributions are highly appreciated! Please submit issues or pull requests to help make this project better.

## 📜 License

This project is open-source under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 🙏 Acknowledgments

Big thanks to the developers of **Emergency Response: Liberty County** for providing this API and creating an incredible role-playing experience.
