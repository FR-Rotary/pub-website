import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		allowedHosts: ["rotary.kryddan.xyz"],
		host: "0.0.0.0"
	}
});
