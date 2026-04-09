use serde::{Deserialize, Serialize};

// WebSocket JSON schema: keep tag names and field names aligned with `frontend/src/lib/ipc.ts`
// (`handleEvent` / `sendAction`). See also `design/ROADMAP.md` P1.4.

// Events sent from jarvis-app to GUI
#[derive(Clone, Debug, Serialize)]
#[serde(tag = "event", rename_all = "snake_case")]
pub enum IpcEvent {
    // Wake word detected, starting to listen
    WakeWordDetected,
    
    // Actively listening for command
    Listening,
    
    // Speech recognized
    SpeechRecognized { text: String },
    
    // Command was executed
    CommandExecuted { id: String, success: bool },
    
    // Returned to idle state
    Idle,
    
    // Error occurred
    Error { message: String },
    
    // App started
    Started,
    
    // App is shutting down
    Stopping,
    
    // Pong response
    Pong,

    // request GUI to reveal/focus window
    RevealWindow,

    /// Mic listening muted or unmuted (wake word + voice commands paused when muted).
    MicMuted { muted: bool },

    /// Command packs were reloaded from disk (after successful parse + intent refresh).
    CommandsReloaded { command_packs: usize },
}

// Actions sent from GUI to jarvis-app
#[derive(Clone, Debug, Deserialize)]
#[serde(tag = "action", rename_all = "snake_case")]
pub enum IpcAction {
    // Request graceful shutdown
    Stop,
    
    // Reload commands from disk
    ReloadCommands,
    
    // Ping to check connection
    Ping,
    
    // Mute/unmute listening
    SetMuted { muted: bool },

    // Execute text command
    TextCommand { text: String },
}