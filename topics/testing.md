# Testing & verification loop

1. `VerseToolset.BuildAll` → must be `[]`.
2. `CompileWidgetBlueprint` → must be `true` (errors are raised with the binding path).
3. Session:
```python
S='ValkyrieToolset.SessionToolset.'
if T(S+'GetSessionStatus',{})['returnValue']=='Connected': T(S+'PushChanges',{'bVerseOnly':False})
else: T(S+'StartSession',{})
if T(S+'GetGameState',{})['returnValue']=='Running': T(S+'StopGame',{})
# poll until 'CanStart', then
T(S+'StartGame',{})
```
   `PushChanges(bVerseOnly=True)` is much faster when only Verse changed.
4. Look at the client: `scripts/windows/capture_fortnite_window.ps1 -Out frame.png` (PrintWindow; works behind other windows).
   Capture a burst (e.g. 30 frames × 250 ms) and build a contact sheet to judge animations.
5. You **cannot click** in the client (SendInput is ignored). Add debug device options (auto-open, auto-claim, short day length,
   reset save on join) to drive flows, and ask the human to test real clicks/hover/Escape.
6. Put `Print("[Feature] ...")` on every click handler — the user can grep the editor Output Log to tell
   "click didn't arrive" from "logic failed".
7. Restore production settings afterwards and say so.

Debug options in the daily reward device: `SecondsPerDay`, `ResetProgressOnJoin`, `DebugAutoClaimAfter`, `AutoOpenOnJoin`, `AutoCloseAfter`.
