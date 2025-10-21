import { request } from "../utils/request.js";

export async function run() {
  return await request("/memory/stats");
}
