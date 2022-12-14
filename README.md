# Quick Start

Use the Lighthouse provider plugin to interact with the [Ethereum consensus layer](https://github.com/ethereum/beacon-APIs) via a [Lighthouse](https://github.com/sigp/lighthouse) consensus client.

## Dependencies

* [python3](https://www.python.org/downloads) version 3.8 or greater, python3-dev

## Installation

### via `pip`

You can install the latest release via [`pip`](https://pypi.org/project/pip/):

```bash
pip install ape-lighthouse
```

### via `setuptools`

You can clone the repository and use [`setuptools`](https://github.com/pypa/setuptools) for the most up-to-date version:

```bash
git clone https://github.com/ApeWorX/ape-lighthouse.git
cd ape-lighthouse
python3 setup.py install
```

## Quick Usage

```
ape console --network beacon:mainnet:lighthouse
```

## Development

This project is in development and should be considered a beta.
Things might not be in their final state and breaking changes may occur.
Comments, questions, criticisms and pull requests are welcomed.
