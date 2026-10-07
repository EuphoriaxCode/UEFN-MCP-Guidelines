# ValkyrieToolset.SessionToolset

Drives the UEFN play-in-client play-test loop: start and stop a session, push content changes to the
connected server, and start, stop, and inspect the in-game match.

8 tools.

### `GetClientLogEntries`

Search the launched client's log for a pattern, case-insensitively.

| arg | type | req | description |
|---|---|---|---|
| `pattern` | `string` | yes | A regular expression matched against each line (e.g. "frame [0-9]+"). |
| `maxResults` | `integer` |  | Maximum matches to return; unset means unlimited. (default `null`) |
| `startLine` | `integer` |  | 0-indexed line to start from; negative starts at the first line. (default `0`) |

Returns: `SessionToolsetClientLogEntries{entries:[string], lastEntryLine:integer}`

### `GetGameState`

Get the state of the in-game match on the connected server.

Returns: `CanStart or Running or Unconnected`

### `GetSessionStatus`

Get the connection status of the play-in-client session.

Returns: `Disconnected or Connecting or Reconnecting or Connected or UpdatingContent`

### `PushChanges`

Re-send modified project data to the connected server.

| arg | type | req | description |
|---|---|---|---|
| `bVerseOnly` | `boolean` |  | Send only modified Verse source, skipping the asset cook a full push performs; much faster, so prefer it when only Verse changed. (default `false`) |

Returns: `Failed or Completed or StillRunning`

### `StartGame`

Start the in-game match on the connected server.

Returns: `Failed or Completed or StillRunning`

### `StartSession`

Upload the open project and launch a play-in-client session.

| arg | type | req | description |
|---|---|---|---|
| `location` | `Vector{x:number, y:number, z:number}` |  | When set, launches via Play From Here: starts a match and spawns the player at this position once content finishes loading. (default `null`) |
| `rotation` | `Rotator{pitch:number, yaw:number, roll:number}` |  | Spawn orientation applied with Location; ignored when Location is unset. (default `null`) |

Returns: `Failed or Completed or StillRunning`

### `StopGame`

Stop the running in-game match on the connected server.

Returns: `Failed or Completed or StillRunning`

### `StopSession`

Disconnect from and tear down the active play-in-client session.
