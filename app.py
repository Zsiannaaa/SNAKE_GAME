import webview
import sys
import os

def get_html_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), 'snake.html')
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'snake.html')

if __name__ == '__main__':
    html_path = get_html_path()
    window = webview.create_window(
        'Snake++ · Auto-pilot Edition',
        url=html_path,
        width=700,
        height=850,
        resizable=False,
        min_size=(400, 600),
    )
    webview.start()
