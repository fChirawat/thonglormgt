import path from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import proxyOptions from './proxyOptions';
import tailwindcss from '@tailwindcss/vite'

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [vue(), tailwindcss(),
	],
	server: {
		port: 8080,
		host: '0.0.0.0',
		proxy: proxyOptions
	},
	resolve: {
		alias: {
			'@': path.resolve(__dirname, 'src')
		}
	},
	build: {
		outDir: '../thonglormgt/public/inspector',
		emptyOutDir: true,
		target: 'es2015',
	},
	// '/api': {
  //   target: 'http://localhost:8001',
  //   changeOrigin: true,
  //   secure: false,
  //   rewrite: (path) => path.replace(/^\/api/, '/api')
  // },
});




// import path from 'path';
// import { defineConfig } from 'vite';
// import vue from '@vitejs/plugin-vue';
// import tailwindcss from '@tailwindcss/vite';

// export default defineConfig({
//   plugins: [vue(), tailwindcss()],
//   server: {
//     port: 8080,
//     host: '0.0.0.0',
//     proxy: {
//       '/api': {
//         target: 'http://localhost:8001',
//         changeOrigin: true,
//         secure: false,
//         rewrite: path => path.replace(/^\/api/, '/api')
//       }
//     }
//   },
//   resolve: {
//     alias: {
//       '@': path.resolve(__dirname, 'src')
//     }
//   },
// });

