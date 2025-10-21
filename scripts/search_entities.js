import { request } from "../utils/request.js";

export async function run(input) {
  if (!input || !input.query) {
    throw new Error("Missing query");
  }
  const query = encodeURIComponent(input.query);
  return await request(`/memory/search?q=${query}`);
}
