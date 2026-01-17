use std::path::PathBuf;

// Context passed to Lua scripts
#[derive(Debug, Clone)]
pub struct CommandContext {
    // The phrase that triggered the command
    pub phrase: String,
    
    // Command ID
    pub command_id: String,

    // Path to command folder
    pub command_path: PathBuf,

    // Current language
    pub language: String,
}

// Result returned from Lua script execution
#[derive(Debug, Clone)]
pub struct CommandResult {
    // Whether to continue chaining commands
    pub chain: bool,
}

impl Default for CommandResult {
    fn default() -> Self {
        Self { chain: true }
    }
}