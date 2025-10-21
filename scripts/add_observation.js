import { request } from "../utils/request.js";

export async function run(input) {
  if (!input || !input.entity_name || !input.content) {
    throw new Error("Missing entity_name or content");
  }
  const payload = {
    entity_name: input.entity_name,
    content: input.content,
    source: input.source || "claude-skill"
  };
  return await request("/memory/observation", "POST", payload);
}
