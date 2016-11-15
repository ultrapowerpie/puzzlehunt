from flask_assets import Bundle, Environment

bundles = {

    'style': Bundle(
        'css/lib/bootstrap-responsive.min.css',
        'css/lib/bootstrap.min.css',
        'css/style.css',
        output='gen/style.css'),

    'clockStyle': Bundle(
        'css/lib/flipclock.css',
        output='gen/clockStyle.css'),

    'script': Bundle(
        'js/lib/jquery.min.js',
        'js/lib/bootstrap.min.js',
        output='gen/script.js'),

    'scratch': Bundle(
        'js/scratch.js',
        output='gen/scratch.js'),

    'clock': Bundle(
        'js/lib/flipclock.min.js',
        'js/countdown.js',
        output='gen/clock.js')
}
