const path = require('path');

module.exports = {
	webpack: {
		alias: {
			'@': path.resolve(__dirname, 'src'),
			'@components': path.resolve(__dirname, 'src/assets/Components'),
			'@customTypes': path.resolve(__dirname, 'src/customTypes'),
			'@context': path.resolve(__dirname, 'src/context'),
			'@lib': path.resolve(__dirname, 'src/lib'),
			'@modules': path.resolve(__dirname, 'src/modules'),
			'@ui': path.resolve(__dirname, 'src/assets/Components/ui'),
		},
	}
}