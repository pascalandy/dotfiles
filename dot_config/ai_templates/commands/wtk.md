   ---
   description: wtk
   ---
   Use the subagent tool with the chain parameter to execute this workflow:

   1. Use the @scout agent to analyze the codebase for: $@
   2. Then use the @general agent to tell me what I should know about this project within two or three sentences, using {previous}

   Execute this as a chain, passing output between steps via {previous}