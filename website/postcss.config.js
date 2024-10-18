module.exports = {
  plugins: [
    require('@fullhuman/postcss-purgecss')({
      content: [
        'rotary/templates/**/*.html',
        'rotary/static/js/**/*.js'
      ],
      defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || []
    })
  ]
};