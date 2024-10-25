# R6-Stats-Bot
A Discord bot for viewing &amp; tracking R6 Siege stats.

# Development

It is recommended to use a Python virtual environment.

### Set Environment
| Name                 | Required | Default             | Description |
|----------------------|----------|---------------------|-------------|
| BASE_TRACKER_API_URL | &#9745;  |                     | The base API URL to retrieve stats from. |
| DISCORD_BOT_TOKEN    | &#9745;  |                     | The token of the R6 Stats Discord Bot. |
| DISCORD_GUILD_TOKEN  |          | `GUILD-ID-GUILD-ID` | The Server/Guild ID to connect to. |
| LOG_LEVEL            |          | `INFO`              | Level of logging to display/save. Can be one of `DEBUG`, `INFO`, `WARN`, `ERROR` |

### Install Dependencies
`poetry install --with dev`

### Activate Bot
`python -m bot`
