# ValkyrieToolset.VerseToolset

Reads, searches, edits, and compiles the Verse source of the open UEFN project. File tools act on
.verse files addressed by their Verse path (e.g. `/<project>/Sub/Foo.verse`). That root is project-
specific -- it is not `/Game` -- so pass `""` to address the root itself, and build paths from the ones
the listing and search tools return. Read-only verse digests are accessible through `/<VRI> (Name)`.

10 tools.

### `BuildAll`

Compile all Verse code in the project.

Returns: `[VerseToolsetDiagnostic]`

### `Copy`

Copy a .verse file, or a directory whose subtree contains only .verse files.

| arg | type | req | description |
|---|---|---|---|
| `sourcePath` | `string` | yes | Source path. A file source (and its dest) must be a .verse file; a directory source's subtree must contain no non-.verse file. |
| `destPath` | `string` | yes | Destination; must not already exist; parent must exist; may not be inside a directory source. |
| `bRecursive` | `boolean` | yes | Required (true) when the source is a directory. |

### `CreateDirectory`

Create a directory, including any missing parent directories.

| arg | type | req | description |
|---|---|---|---|
| `path` | `string` | yes | Directory path to create. |

### `Delete`

Delete a .verse file, or a directory whose subtree contains only .verse files.

| arg | type | req | description |
|---|---|---|---|
| `path` | `string` | yes | Path to delete. A file path must be a .verse file; a directory's subtree must contain no non-.verse file. The workspace root is rejected. |
| `bRecursive` | `boolean` | yes | Delete a non-empty directory recursively. |

### `Grep`

Search .verse files for a pattern.

| arg | type | req | description |
|---|---|---|---|
| `pattern` | `string` | yes | Text to find. A literal substring, matched case-insensitively — unless it is wrapped in '/' (e.g. "/foo.*bar/"), in which case the text between the slashes is a per-line, case-sensitive regular expression (use an inline "(?i)" for case-insensitive regex). |
| `pathGlob` | `string` | yes | Glob restricting which files are searched ("" = every .verse file ListFiles can reach). '*' and '?' match within a single path segment; a '**' segment matches across directories. A bare "*" will not match anything as there are no top-level files; lead with a '**' segment to match .verse files at any depth. |
| `maxResults` | `integer` |  | Maximum matches to return; unset means unlimited. (default `null`) |

Returns: `[VerseToolsetGrepMatch{filePath:string, span:VerseToolsetSourceSpan{startLine:integer, startCharacter:integer, endLine:integer, endCharacter:integer}, lineText:string}]`

### `ListFiles`

List a directory's .verse files and subdirectories (other files are omitted).

| arg | type | req | description |
|---|---|---|---|
| `path` | `string` | yes | Directory path to list. An empty path ("") lists the project's own top-level Verse package plus the read-only generated digest packages it depends on, each as a directory entry. |
| `bRecursive` | `boolean` | yes | Descend into subdirectories. |

Returns: `[VerseToolsetFileEntry{name:string, type:File or Directory}]`

### `Move`

Move/rename a .verse file, or a directory whose subtree contains only .verse files.

| arg | type | req | description |
|---|---|---|---|
| `sourcePath` | `string` | yes | Source path. A file source (and its dest) must be a .verse file; a directory source's subtree must contain no non-.verse file. |
| `destPath` | `string` | yes | Destination; must not already exist; parent must exist; may not be inside a directory source. |

### `ReadFile`

Read a .verse file.

| arg | type | req | description |
|---|---|---|---|
| `path` | `string` | yes | Path to a .verse file. |
| `span` | `VerseToolsetSourceSpan{startLine:integer, startCharacter:integer, endLine:integer, endCharacter:integer}` |  | Region to read. Unset reads the whole file. Out-of-range positions are clamped. (default `null`) |

Returns: `string`

### `Replace`

Replace OldString with NewString in a .verse file.

| arg | type | req | description |
|---|---|---|---|
| `path` | `string` | yes | Path to a .verse file. |
| `oldString` | `string` | yes | Existing text to find. |
| `newString` | `string` | yes | Replacement text. |
| `bReplaceAll` | `boolean` |  | Replace every occurrence. When false, OldString must occur exactly once. (default `false`) |

### `WriteFile`

Create, overwrite, or edit a region of a .verse file.

| arg | type | req | description |
|---|---|---|---|
| `path` | `string` | yes | Path to a .verse file. |
| `content` | `string` | yes | Text to write; empty deletes the target region (or empties the file). No separator is inserted around the written region, so include a leading "\n" when starting a new line. |
| `span` | `VerseToolsetSourceSpan{startLine:integer, startCharacter:integer, endLine:integer, endCharacter:integer}` |  | What to write. Unset overwrites the whole file. A span replaces that region of an existing file; a zero-width span inserts without replacing (an end-of-file span therefore appends). (default `null`) |
| `bCreateIfMissing` | `boolean` | yes | Create the file (and parent directories) when it does not exist. Applies to a whole-file write or an end-of-file append, not to a region replace. |
