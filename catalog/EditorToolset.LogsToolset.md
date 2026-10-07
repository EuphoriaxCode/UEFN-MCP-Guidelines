# EditorToolset.LogsToolset

Provides tools for reading the Unreal Engine output log and controlling
log category verbosity.

4 tools.

### `GetLogCategories`

Returns a sorted list of registered log categories.

| arg | type | req | description |
|---|---|---|---|
| `filter` | `string` |  | If non-empty, only returns categories whose name contains this substring. (default `""`) |

Returns: `[string]`

### `GetLogEntries`

Returns log entries from the current session's log file.

| arg | type | req | description |
|---|---|---|---|
| `category` | `string` |  | If non-empty, only returns entries from this log category (e.g. "LogTemp"). (default `"LogsToolset"`) |
| `pattern` | `string` |  | If non-empty, only returns entries whose text matches this regular expression. (default `""`) |
| `maxEntries` | `integer` |  | Maximum number of entries to return, taken from the end of the log. Pass 0 for no limit. Defaults to 1000. (default `1000`) |

Returns: `[string]`

### `GetVerbosity`

Returns the current verbosity level for a log category.

| arg | type | req | description |
|---|---|---|---|
| `category` | `string` |  | The log category name, e.g. "LogTemp". (default `"LogsToolset"`) |

Returns: `string`

### `SetVerbosity`

Sets the verbosity level for a log category.

| arg | type | req | description |
|---|---|---|---|
| `category` | `string` |  | The log category name, e.g. "LogTemp". (default `"LogsToolset"`) |
| `verbosity` | `string` | yes | The verbosity level: one of "NoLogging", "Fatal", "Error", "Warning", "Display", "Log", "Verbose", or "VeryVerbose". |
