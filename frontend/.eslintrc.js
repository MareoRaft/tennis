module.exports = {
	'env': {
		'browser': true,
		'es6': true,
	},
	'extends': [
		'eslint:recommended',
		'plugin:react/recommended',
	],
	'globals': {
		'Atomics': 'readonly',
		'SharedArrayBuffer': 'readonly',
	},
	'parserOptions': {
		'ecmaFeatures': {
			'jsx': true,
		},
		'ecmaVersion': 2018,
		'sourceType': 'module',
	},
	'plugins': [
		'react',
	],
	'settings': {
		'react': {
			'createClass': 'createReactClass',
			'pragma': 'React',
			'version': 'detect',
		},
		'propWrapperFunctions': [
			'forbidExtraProps',
			{
				'property': 'freeze',
				'object': 'Object',
			},
			{
				'property': 'myFavoriteWrapper',
			},
		],
		'linkComponents': [
			'Hyperlink',
			{
			'name': 'Link',
			'linkAttribute': 'to',
			},
		],
	},
	'rules': {
		'indent': [
			'error',
			'tab',
		],
		'linebreak-style': [
			'error',
			'unix',
		],
		'quotes': [
			'error',
			'single',
		],
		'semi': [
			'error',
			'always',
		],
	},
};
