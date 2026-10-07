# ValkyrieToolset.ValkyriePythonToolset

Enables and checks Python for the current UEFN project. The core engine Python toolsets (actor,
object, scene, asset) only load once Python is enabled, so enable it first when they are missing.

2 tools.

### `EnablePythonInUEFN`

Enable Python for the active UEFN project. Enablement is ASYNCHRONOUS: the core Python toolsets
appear after the editor next ticks, not immediately on return - re-list toolsets / retry before
assuming failure. Raises if there is no active project or the Python setting is unavailable.

### `IsPythonEnabledInUEFN`

Whether the main UEFN project has Python enabled and the interpreter is initialized. Enablement follows
the main project alone: a referenced project's saved setting is loaded but never applied.

Returns: `boolean`
