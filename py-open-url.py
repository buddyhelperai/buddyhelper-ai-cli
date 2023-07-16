import gi
gi.require_version("Gtk", "3.0")
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2, Gdk
import re
from datetime import datetime

import requests
import json

def openurl(url):
        window = BrowserWindow()
        window.show_all()
        window.load_url(url)
        Gtk.main()

#web-browser
class ConfirmDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Confirmation", parent, Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT, 
        (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        ))

        self.set_default_size(150, 100)

        label = Gtk.Label("Confirm that you are allowed to grab the selected content to train your AI")

        box = self.get_content_area()
        box.add(label)
        self.show_all()

class BrowserWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Simple Browser")
        self.set_default_size(800, 600)

        self.webview = WebKit2.WebView()
        self.add(self.webview)

        self.connect("destroy", Gtk.main_quit)
        self.connect("key-press-event", self.on_key_press)

    def load_url(self, url):
        self.webview.load_uri(url)

    def on_key_press(self, widget, event):
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
        if ctrl and event.keyval == Gdk.KEY_c:
            dialog = ConfirmDialog(self)
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                self.webview.run_javascript("window.getSelection().toString();", None, self.on_get_selected_text, None)
                #self.webview.run_javascript("""
                #function getSelectedHTML() {
                #    var sel = window.getSelection();
                #    var range = sel.getRangeAt(0);
                #    var div = document.createElement('div');
                #    div.appendChild(range.cloneContents());
                #    var elements = div.getElementsByTagName("*");
                #    for (var i = 0; i < elements.length; i++) {
                #        var tagName = elements[i].tagName.toLowerCase();
                #        if (tagName !== 'p' && tagName !== 'h1' && tagName !== 'h2' && tagName !== 'h3' && tagName !== 'ul' && tagName !== 'li') {
                #            elements[i].outerHTML = elements[i].innerHTML;
                #        }
                #    }
                #    return div.innerHTML;
                #}
                #getSelectedHTML();
                #""", None, self.on_get_selected_text, None)
            elif response == Gtk.ResponseType.CANCEL:
                print("Cancel clicked")

            dialog.destroy()

    def on_get_selected_text(self, webview, result, user_data):
        js_result = webview.run_javascript_finish(result)
        if js_result is not None:
            selected_text = js_result.get_js_value().to_string()
            current_url = webview.get_uri()
            # Remove all non-alphanumeric characters and convert to lowercase
            filename = re.sub(r'\W+', '', current_url).lower()
            # Add current date and time to the filename
            current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            with open(f"./data/{filename}-{current_time}.html", "w") as f:
                f.write(selected_text)
#web-browser--


while True:
    url = input("Url: ")
    openurl(url)
