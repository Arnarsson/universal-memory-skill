import { request } from "../utils/request.js";

export async function run(input) {
  if (!input || !input.entity_name) {
    throw new Error("Missing entity_name");
  }
  const entityName = encodeURIComponent(input.entity_name);
  return await request(`/memory/graph/${entityName}`);
}
