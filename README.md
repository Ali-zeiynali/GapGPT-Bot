# GapGPT-Bot

Legacy Python experiments for communicating with GapGPT's web chat over WebSocket. This is an unofficial prototype, not an official SDK or a stable API integration.

## Setup

Use Python 3.10 or newer:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item credentials.example.json credentials.local.json
```

Fill in the local credentials file with credentials for your own account, or supply the corresponding environment variables:

- `GAPGPT_ACCESS_TOKEN`: access token for the synchronous scripts.
- `GAPGPT_CHAT_TOKEN`: chat identifier for the synchronous scripts.
- `GAPGPT_ASYNC_ACCESS_TOKEN`: optional separate token for the asynchronous experiment; falls back to `GAPGPT_ACCESS_TOKEN`.

`credentials.local.json` and `cookies.json` are excluded from Git. Existing local credentials are preserved when preparing this repository.

## Scripts

- `main.py`: interactive synchronous chat experiment.
- `test.py`: sends several experimental payload formats to the service.
- `test_2.py`: asynchronous streaming experiment.
- `test.html`: captured HTML shell used while investigating the web client; its referenced website assets are not bundled.

These scripts use a website-specific, undocumented protocol and may need adjustments as the service changes. Running the network experiments sends messages to the service and can consume account quota. Only syntax and local configuration were checked when preparing the repository; no live service test was performed.

The legacy synchronous experiments disable TLS certificate verification. They are retained as experimental source and should be reviewed before use on an untrusted network.
