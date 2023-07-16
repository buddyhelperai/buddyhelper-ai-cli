import gi
gi.require_version("Gtk", "3.0")
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2, Gdk
import re
from datetime import datetime

import requests
import json

google_api_key = "[your-google-api-key]"

cx_searchengineid  = "[your-search-engine-id]" #https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
geolocation = "it" #https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
country = "countryIT" #https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
lang_result = "lang_it" #https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
google_lang = "it" #https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
num = 3; #https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list

def search_googleserp(query):
    url = "https://customsearch.googleapis.com/customsearch/v1"
    querystring = {
        "key": google_api_key,
        "cr": country,
        "cx": cx_searchengineid,
        "gl": geolocation,
        "lr": lang_result,
        "num": num,
        "q": query
    }

    response = requests.request("GET", url, params=querystring)

    data = json.loads(response.text)

    items = data['items']

    for index, item in enumerate(items):
        print(f"({index}) Title: {item['title']}")
        print(f"Link: {item['link']}")
        #print(f"Snippet: {item['snippet']}\n")

    while True:
        browseurlindex = input("Website index: ")
        browseurlindex = int(browseurlindex)
        print(items[browseurlindex])

        window = BrowserWindow()
        window.show_all()
        window.load_url(items[browseurlindex]['link'])
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
    query = input("Query: ")
    search_googleserp(query)
