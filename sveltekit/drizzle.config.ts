import { defineConfig } from "drizzle-kit";

export default defineConfig({
	dialect: "sqlite",
	dbCredentials: {
		url: "/home/node/instance/rotary.sqlite",
	},
	out: "./src/lib/server/db/drizzle",
	schema: "./src/lib/server/db/*"
});
