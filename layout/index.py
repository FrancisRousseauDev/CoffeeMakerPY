from dash import dcc
from dash import html
import base64


def showHTML(app):
    # define layout of screen

    app.layout = html.Div([

        html.Link(
            rel='stylesheet',
            href='/assets/css/stylesheet.css'
        ),

        html.Div([
            html.Div([
                html.Img(src='data:image/gif;base64,{}'.format(encodeImage('assets/images/gif.gif').decode())),
            ], className='header-text')

        ], className='header'),

        html.Div([
            html.Img(src='data:image/gif;base64,{}'.format(encodeImage('assets/images/noCoffeeNoCoding.png').decode()),
                     className='image first'),

            html.Div([
                html.P(children='An app to analyze all data around coffee'),
                html.P(children='Interested?')
            ], className='textContainer'),

            html.Img(src='data:image/png;base64,{}'.format(encodeImage('assets/images/qrcode.png').decode()),
                     className='image'),

        ], className='flex'),

        html.Div([
            html.Div([], className='seperator'),
            html.P(children='Made by Francis from Bingli', className='footerText'),

        ], className='footer'),
    ])


def encodeImage(imageName):
    return base64.b64encode(open(imageName, 'rb').read())
