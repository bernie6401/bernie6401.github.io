source 'https://rubygems.org'
gem 'github-pages', group: :jekyll_plugins
#gem 'jekyll-admin', group: :jekyll_plugins
gem 'wdm', '>= 0.1.0' if Gem.win_platform?
gem 'faraday-retry'
gem 'jekyll-algolia'
gem "jekyll", "~> 3.9.4"

# csv and bigdecimal move out of Ruby's default gems starting in 3.4.0; jekyll/liquid
# still require them, so declare them explicitly to silence the stdlib warning.
gem 'csv'
gem 'bigdecimal'

# webrick was removed from Ruby's default gems in 3.0.0; `jekyll serve` needs it
# for its dev server, so declare it explicitly or `jekyll s` fails to boot.
gem 'webrick'