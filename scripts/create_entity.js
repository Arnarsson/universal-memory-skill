import { request } from "../utils/request.js";

export async function run(input) {
  if (!input || !input.name || !input.type) {
    throw new Error("Missing name or type");
  }
  return await request("/memory/entity", "POST", input);
}
